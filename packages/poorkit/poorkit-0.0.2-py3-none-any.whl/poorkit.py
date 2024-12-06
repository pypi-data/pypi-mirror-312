from click import *
import file
import pkg_resources

version = pkg_resources.require("poorkit")[0].version

help = f"""poorkit {version}\n
Reference: https://pypi.org/project/poorkit
"""


@group(help=help)
def cli() -> None:
    pass


cli.add_command(file.file)
