import os
from click import *


@group()
def file() -> None:
    pass


@command(help="creating a file")
@option("--name", help="name of the file", required=True)
@option("--content", help="content of the file", required=False)
def create(name: str, content: str) -> None:
    with open(name, "w", encoding="utf-8") as f:
        if content:
            f.write(content)


@command(help="cat a file")
@argument("name", required=True)
def cat(name: str) -> None:
    if not os.path.exists(name):
        print(f"file not found: {name}")
        return
    with open(name, "r", encoding="utf-8") as f:
        print(f.read())


@command(help="delete a file")
@argument("name", required=True)
def delete(name: str) -> None:
    os.remove(name)


@command(help="rename a file")
@argument("name", required=True)
@argument("new_name", required=True)
def mv(name: str, new_name: str) -> None:
    os.rename(name, new_name)


@command(help="copy a file")
@argument("name", required=True)
@argument("new_name", required=True)
def cp(name: str, new_name: str) -> None:
    with open(name, "r", encoding="utf-8") as f:
        with open(new_name, "w", encoding="utf-8") as nf:
            nf.write(f.read())


# list files
@command(help="list files")
@option("-a", "--show-all", is_flag=True, help="show hidden files")
@option("-l", "--show-list", is_flag=True, help="show files in a list")
def ls(show_all, show_list) -> None:
    if not show_list:
        print("  ".join(os.listdir()))
    else:
        for file in os.listdir():
            print(file)


file.add_command(create)
file.add_command(delete)
file.add_command(cat)
file.add_command(mv)
file.add_command(cp)
file.add_command(ls)
