import importlib.metadata
from pathlib import Path
from shutil import copy2, copytree

from pydantic import DirectoryPath, validate_call

from sereto.cli.utils import Console
from sereto.exceptions import SeretoPathError
from sereto.jinja import render_j2
from sereto.models.config import Config, VersionConfig
from sereto.models.project import Project
from sereto.models.settings import Settings
from sereto.models.version import ProjectVersion, SeretoVersion
from sereto.pdf import render_finding_group_pdf, render_report_pdf, render_target_pdf
from sereto.plot import risks_plot
from sereto.source_archive import create_source_archive, embed_source_archive
from sereto.target import create_findings_config, get_risks, render_target_j2
from sereto.types import TypeProjectId
from sereto.utils import write_if_different


@validate_call
def copy_skel(templates: DirectoryPath, dst: DirectoryPath, overwrite: bool = False) -> None:
    """Copy the content of a templates `skel` directory to a destination directory.

    A `skel` directory is a directory that contains a set of files and directories that can be used as a template
    for creating new projects. This function copies the contents of the `skel` directory located at
    the path specified by `templates` to the destination directory specified by `dst`.

    Args:
        templates: The path to the directory containing the `skel` directory.
        dst: The destination directory to copy the `skel` directory contents to.
        overwrite: Whether to allow overwriting of existing files in the destination directory.
            If `True`, existing files will be overwritten. If `False` (default), a `SeretoPathError` will be raised
            if the destination directory already exists.

    Raises:
        SeretoPathError: If the destination directory already exists and `overwrite` is `False`.
    """
    skel_path: Path = templates / "skel"
    Console().log(f"Copying 'skel' directory: '{skel_path}' -> '{dst}'")

    for item in skel_path.iterdir():
        dst_item: Path = dst / (item.relative_to(skel_path))
        if not overwrite and dst_item.exists():
            raise SeretoPathError("Destination already exists")
        if item.is_file():
            Console().log(f" [green]+[/green] copy file: '{item.relative_to(skel_path)}'")
            copy2(item, dst_item, follow_symlinks=False)
        if item.is_dir():
            Console().log(f" [green]+[/green] copy dir: '{item.relative_to(skel_path)}'")
            copytree(item, dst_item, dirs_exist_ok=overwrite)


@validate_call
def new_report(settings: Settings, id: TypeProjectId, name: str) -> None:
    """Generates a new report with the specified ID.

    Args:
        settings: Global settings.
        id: The ID of the new report. This should be a string that uniquely identifies the report.
        name: The name of the new report.

    Raises:
        SeretoValueError: If a report with the specified ID already exists in the `reports` directory.
    """
    Console().log(f"Generating a new report with ID {id!r}")

    if (new_path := (settings.reports_path / id)).exists():
        raise SeretoPathError("report with specified ID already exists")
    else:
        new_path.mkdir()

    sereto_ver = importlib.metadata.version("sereto")

    cfg = Config(
        sereto_version=SeretoVersion.from_str(sereto_ver),
        version_configs={
            ProjectVersion.from_str("v1.0"): VersionConfig(
                id=id,
                name=name,
            ),
        },
    )

    Console().log("Copy report skeleton")
    copy_skel(templates=settings.templates_path, dst=new_path)

    config_path: Path = new_path / "config.json"
    Console().log(f"Writing the config '{config_path}'")
    with config_path.open("w", encoding="utf-8") as f:
        f.write(cfg.model_dump_json(indent=2))


@validate_call
def render_report_j2(
    project: Project,
    version: ProjectVersion,
    convert_recipe: str | None = None,
) -> None:
    """Renders Jinja templates into TeX files.

    This function processes Jinja templates for report, approach and scope in each target, and all relevant findings.

    Args:
        project: Project's representation.
        version: The version of the report which should be rendered.
        convert_recipe: Name which will be used to pick a recipe from Render configuration. If none is provided, the
            first recipe with a matching format is used.
    """
    cfg = project.config.at_version(version=version)

    # Render dependencies
    for target in cfg.targets:
        render_target_j2(target=target, project=project, version=version, convert_recipe=convert_recipe)

    # Find the report template
    report_j2_path = project.path / f"report{version.path_suffix}.tex.j2"
    if not report_j2_path.is_file():
        raise SeretoPathError(f"template not found: '{report_j2_path}'")

    # Prepare the config for Jinja
    # make shallow dict - values remain objects on which we can call their methods in Jinja
    cfg_dict = {key: getattr(cfg, key) for key in cfg.model_dump()}

    # Render the Jinja template
    report_generator = render_j2(
        templates=project.path,
        file=report_j2_path,
        vars={"c": cfg, "config": project.config, "version": version, "report_path": project.path, **cfg_dict},
    )

    # Write the rendered template to a file
    report_path = report_j2_path.with_suffix("")
    write_if_different(file=report_path, content="".join(report_generator))
    Console().log(f"Rendered Jinja template: {report_path.relative_to(project.path)}")


@validate_call
def render_sow_j2(project: Project, version: ProjectVersion) -> None:
    cfg = project.config.at_version(version=version)

    # Find the SoW template
    sow_j2_path = project.path / f"sow{version.path_suffix}.tex.j2"
    if not sow_j2_path.is_file():
        raise SeretoPathError(f"template not found: '{sow_j2_path}'")

    # Prepare the config for Jinja
    # make shallow dict - values remain objects on which we can call their methods in Jinja
    cfg_dict = {key: getattr(cfg, key) for key in cfg.model_dump()}

    # Render the Jinja template
    sow_generator = render_j2(
        templates=project.path,
        file=sow_j2_path,
        vars={"c": cfg, "config": project.config, "version": version, "report_path": project.path, **cfg_dict},
    )

    # Write the rendered template to a file
    sow_path = sow_j2_path.with_suffix("")
    write_if_different(file=sow_path, content="".join(sow_generator))
    Console().log(f"Rendered Jinja template: {sow_j2_path.with_suffix('').relative_to(project.path)}")


@validate_call
def report_create_missing(project: Project, version: ProjectVersion) -> None:
    """Creates missing target directories from config.

    This function creates any missing target directories and populates them with content of the "skel" directory from
    templates.

    Args:
        project: Project's representation.
        version: The version of the report.
    """
    cfg = project.config.at_version(version=version)

    for target in cfg.targets:
        assert target.path is not None
        category_templates = project.settings.templates_path / "categories" / target.category

        if not target.path.is_dir():
            Console().log(f"Target directory not found, creating: '{target.path}'")
            target.path.mkdir()
            if (category_templates / "skel").is_dir():
                Console().log(f"""Populating new target directory from: '{category_templates / "skel"}'""")
                copy_skel(templates=category_templates, dst=target.path)
            else:
                Console().log(f"No 'skel' directory found: '{category_templates}'")

            create_findings_config(target=target, project=project, templates=category_templates / "findings")

        risks = get_risks(target=target, version=version)
        risks_plot(risks=risks, path=target.path / "risks.png")

        for finding_group in target.findings_config.finding_groups:
            finding_group_j2_path = target.path / "findings" / f"{finding_group.uname}.tex.j2"
            if not finding_group_j2_path.is_file():
                copy2(category_templates / "finding_group.tex.j2", finding_group_j2_path, follow_symlinks=False)


@validate_call
def report_pdf(
    project: Project,
    version: ProjectVersion,
    report_recipe: str | None = None,
    target_recipe: str | None = None,
    finding_recipe: str | None = None,
) -> None:
    cfg = project.config.at_version(version=version)

    for target in cfg.targets:
        render_target_pdf(project=project, target=target, version=version, recipe=target_recipe)

        for finding_group in target.findings_config.finding_groups:
            render_finding_group_pdf(
                project=project,
                finding_group=finding_group,
                target=target,
                version=version,
                recipe=finding_recipe,
            )

    report_path = render_report_pdf(project=project, version=version, recipe=report_recipe)
    archive_path = create_source_archive(project=project)
    embed_source_archive(archive=archive_path, report=report_path, keep_original=False)


@validate_call
def report_cleanup(
    project: Project,
    version: ProjectVersion,
) -> None:
    cfg = project.config.at_version(version=version)

    for target in cfg.targets:
        (project.path / f"{target.uname}.tex").unlink()

        for finding_group in target.findings_config.finding_groups:
            (project.path / f"{target.uname}_{finding_group.uname}.tex").unlink()

    (project.path / f"report{version.path_suffix}.tex").unlink()
