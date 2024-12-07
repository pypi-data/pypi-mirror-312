from os import DirEntry, PathLike
from pathlib import Path
from typing import List

CANONICAL_SEPARATOR = "\n"


class File:
    name: str
    prefix: Path
    is_dir: bool
    is_hidden: bool
    children: List["File"]

    @property
    def path(self) -> Path:
        return self.prefix / self.name

    @property
    def is_hidden(self) -> bool:
        return self.name.startswith(".")

    @property
    def canonical(self) -> str:
        if not self.is_dir:
            return str(self.path)
        files = [c.canonical for c in self.children]
        files.append(str(self.path) + "/")
        return CANONICAL_SEPARATOR.join(files)

    def add_child(self, child: "File"):
        self.add_children([child])

    def add_children(self, children: List["File"]):
        if not self.is_dir:
            raise Exception("Only directories can have children")
        self.children.extend(children)

    def __str__(self) -> str:
        if self.is_dir:
            return str(self.name) + "/"
        return str(self.name)

    @classmethod
    def from_entry(cls, entry: DirEntry) -> "File":
        name = entry.name
        is_dir = entry.is_dir()
        prefix = Path(entry.path).parent

        return File(name, prefix, is_dir)

    def __init__(self, name: str, prefix: PathLike, is_dir: bool = False):
        self.name = name
        self.is_dir = is_dir
        self.prefix = Path(prefix)

        if is_dir:
            self.children = []
