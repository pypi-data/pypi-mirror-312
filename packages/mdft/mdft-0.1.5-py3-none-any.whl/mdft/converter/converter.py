from pathlib import Path
from typing import List
from urllib.parse import quote

from mdft.file import File
from mdft.util import Options

PADDING_CHAR = "\t"
LIST_ENTRY = "- "


class Converter:
    @classmethod
    def _link_for(cls, file: File, base: Path) -> str:
        path = file.path
        if path.is_relative_to(base):
            path = path.relative_to(base)

        path = quote(str(path))
        return path

    @classmethod
    def _to_md(
        cls, file: File, base: Path, options: Options, level: int = 0
    ) -> List[str]:
        name = file.__str__().replace("_", "\\_")
        if options.link:
            name = f"[{name}]({cls._link_for(file, base)})"

        name = (PADDING_CHAR * level) + LIST_ENTRY + name
        result = [name]

        if not file.is_dir:
            return result

        for child in file.children:
            result.extend(cls._to_md(child, base, options, level + 1))

        return result

    @classmethod
    def to_md(cls, file: File, base: Path, options: Options) -> List[str]:
        if not options.include_root:
            if not file.is_dir:
                raise Exception("Cannot skip root of non-directory file")

            result = []
            for child in file.children:
                result.extend(cls._to_md(child, base, options))
            return result

        return cls._to_md(file, base, options)
