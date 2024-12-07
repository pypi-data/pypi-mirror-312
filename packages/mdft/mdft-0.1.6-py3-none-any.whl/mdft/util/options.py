import re
from typing import List, Optional, Tuple, Type, TypeVar

OPTIONS_RE = r'(!)?([^\s=,]+)(?:=(?:"((?:\\.|[^"])*)"|([^,]+)))?'

STR_INCLUDE_HIDDEN = "include_hidden"
STR_INCLUDE_FILES = "include_files"
STR_INCLUDE_ROOT = "include_root"
STR_MAX_DEPTH = "max_depth"
STR_KEEP_LINE = "keep_line"
STR_FILTER = "filter"
STR_LINK = "link"

T = TypeVar("T")


class Options:
    max_depth: Optional[int] = None
    include_hidden: bool = False
    include_files: bool = True
    include_root: bool = False
    keep_line: bool = True
    filter: bool = True
    link: bool = True

    @classmethod
    def _process_option(cls, target: Type[T], modifier: str, value: str) -> T:
        if target is bool:
            value = target(value) if value else True
            value = not value if modifier.startswith("!") else value
        else:
            if not value:
                raise Exception("Expected value for option")

            if modifier:
                raise Exception("Unexpected modifier for option")

            value = target(value)

        return value

    @classmethod
    def _parse_option(cls, option: str) -> List[Tuple[str, str, str]]:
        matches = re.findall(OPTIONS_RE, option)

        # Match group 2 is the value if captured in quotes
        # Match group 3 is the value otherwise
        matches = [(m[0], m[1], m[2] or m[3]) for m in matches]

        return matches

    @classmethod
    def parse(cls, options: str) -> "Options":
        result = Options()
        options = cls._parse_option(options)

        for option in options:
            modifier = option[0]
            name = option[1]
            value = option[2]

            if name == STR_INCLUDE_HIDDEN:
                result.include_hidden = cls._process_option(bool, modifier, value)
            elif name == STR_INCLUDE_FILES:
                result.include_files = cls._process_option(bool, modifier, value)
            elif name == STR_INCLUDE_ROOT:
                result.include_root = cls._process_option(bool, modifier, value)
            elif name == STR_KEEP_LINE:
                result.keep_line = cls._process_option(bool, modifier, value)
            elif name == STR_MAX_DEPTH:
                result.max_depth = cls._process_option(int, modifier, value)
            elif name == STR_FILTER:
                result.filter = cls._process_option(bool, modifier, value)
            elif name == STR_LINK:
                result.link = cls._process_option(bool, modifier, value)
            else:
                raise Exception(f"Unexpected option: {name}")

        return result
