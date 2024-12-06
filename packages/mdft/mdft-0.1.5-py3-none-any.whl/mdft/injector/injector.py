import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterator, List, Optional, TypeVar

from mdft.converter import Converter
from mdft.util import Blueprint, Line

T = TypeVar("T")


class Injector:
    @classmethod
    def _next_definition(cls, iterator: Iterator[T]) -> Optional[T]:
        try:
            return next(iterator)
        except StopIteration:
            return None

    @classmethod
    def inject_into(cls, path: Path, line_blueprints: List[Line[Blueprint]]):
        source = open(path, "r+")
        result = NamedTemporaryFile("w+", delete=False)

        iterator = line_blueprints.__iter__()
        line_blueprint = cls._next_definition(iterator)
        is_block = False

        index = 0
        for line in source:
            index += 1

            if line_blueprint is not None and index == line_blueprint.number:
                blueprint = line_blueprint.value
                options = blueprint.options
                file = blueprint.file

                content = Converter.to_md(file, path.parent, options)

                if options.keep_line:
                    result.write(line)

                for new_line in content:
                    result.write(new_line)
                    result.write("\n")

                line_blueprint = cls._next_definition(iterator)
                is_block = True
            else:
                if line.strip() == "":
                    is_block = False

                if not is_block:
                    result.write(line)

        os.replace(result.name, path)
