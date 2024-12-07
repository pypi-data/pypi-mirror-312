import os

import click

from zhixin.package.manifest.parser import ManifestParserFactory
from zhixin.package.manifest.schema import ManifestSchema, ManifestValidationError
from zhixin.package.pack import PackagePacker


@click.command("pack", short_help="Create a tarball from a package")
@click.argument(
    "package",
    default=os.getcwd,
    metavar="<source directory, tar.gz or zip>",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.option(
    "-o", "--output", help="A destination path (folder or a full path to file)"
)
def package_pack_cmd(package, output):
    p = PackagePacker(package)
    archive_path = p.pack(output)
    # validate manifest
    try:
        ManifestSchema().load_manifest(
            ManifestParserFactory.new_from_archive(archive_path).as_dict()
        )
    except ManifestValidationError as exc:
        os.remove(archive_path)
        raise exc
    click.secho('Wrote a tarball to "%s"' % archive_path, fg="green")
