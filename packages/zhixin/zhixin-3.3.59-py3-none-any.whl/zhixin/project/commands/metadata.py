import json
import os

import click
from tabulate import tabulate

from zhixin import fs
from zhixin.package.commands.install import install_project_dependencies
from zhixin.project.config import ProjectConfig
from zhixin.project.helpers import load_build_metadata


@click.command(
    "metadata", short_help="Dump metadata intended for IDE extensions/plugins"
)
@click.option(
    "-d",
    "--project-dir",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option("-e", "--environment", "environments", multiple=True)
@click.option("--json-output", is_flag=True)
@click.option("--json-output-path", type=click.Path())
def project_metadata_cmd(project_dir, environments, json_output, json_output_path):
    project_dir = os.path.abspath(project_dir)
    with fs.cd(project_dir):
        config = ProjectConfig.get_instance()
        config.validate(environments)
        environments = list(environments or config.envs())
        build_metadata = load_build_metadata(project_dir, environments)

    if not json_output:
        install_project_dependencies(
            options=dict(
                project_dir=project_dir,
                environments=environments,
            )
        )
        click.echo()

    if json_output or json_output_path:
        if json_output_path:
            if os.path.isdir(json_output_path):
                json_output_path = os.path.join(json_output_path, "metadata.json")
            with open(json_output_path, mode="w", encoding="utf8") as fp:
                json.dump(build_metadata, fp)
            click.secho(f"Saved metadata to the {json_output_path}", fg="green")
        if json_output:
            click.echo(json.dumps(build_metadata))
        return

    for envname, metadata in build_metadata.items():
        click.echo("Environment: " + click.style(envname, fg="cyan", bold=True))
        click.echo("=" * (13 + len(envname)))
        click.echo(
            tabulate(
                [
                    (click.style(name, bold=True), "=", json.dumps(value, indent=2))
                    for name, value in metadata.items()
                ],
                tablefmt="plain",
            )
        )
        click.echo()

    return
