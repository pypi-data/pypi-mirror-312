from click import *
import file


@group()
def cli() -> None:
    pass


cli.add_command(file.file)
