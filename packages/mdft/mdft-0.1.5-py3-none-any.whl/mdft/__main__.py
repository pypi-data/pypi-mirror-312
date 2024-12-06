import argparse
from os import PathLike
from pathlib import Path

from mdft.injector import Injector
from mdft.scanner import FileFilter, FileScanner
from mdft.util import Blueprint, Command, Line


def process_file(path: PathLike):
    path = Path(path)

    # Find filter for current path
    filter = FileFilter.for_path(path, ".gitignore")

    # Retrieve all commands from the file
    line_commands = Command.for_file(Path(path))
    if len(line_commands) == 0:
        return

    # Calculate all the file trees
    line_blueprints = []
    for line_command in line_commands:
        file = FileScanner.scan(line_command.value, filter)
        blueprint = Blueprint(file, line_command.value.options)
        line_blueprints.append(Line(blueprint, line_command.number))

    # Inject Blueprints into file
    Injector.inject_into(path, line_blueprints)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MDFT")
    parser.add_argument("path", help="Path to the .md file to be processed")
    arguments = parser.parse_args()

    try:
        process_file(arguments.path)
    except Exception as e:
        print(f"[!] {e}")
        exit(1)
