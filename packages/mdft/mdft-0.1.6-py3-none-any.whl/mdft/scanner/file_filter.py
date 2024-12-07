from pathlib import Path

from pathspec import PathSpec


class FileFilter:
    filters: PathSpec = None

    def does_filter(self, path: Path) -> bool:
        if self.filters is None:
            return False

        path_str = str(path)
        if path.is_dir():
            path_str += "/"

        return self.filters.check_file(path_str).include is True

    @classmethod
    def from_file(cls, path: Path) -> "FileFilter":
        result = FileFilter()

        with open(path, "r+") as file:
            patterns = file.read().splitlines()
            result.filters = PathSpec.from_lines("gitwildmatch", patterns)

        return result

    @classmethod
    def for_path(cls, path: Path, file: str) -> "FileFilter":
        current_path = path.resolve()

        if current_path.is_file():
            current_path = current_path.parent

        file_path = current_path / file
        if file_path.exists():
            return FileFilter.from_file(file_path)

        for parent in current_path.parents:
            file_path = parent / file
            if file_path.exists():
                return FileFilter.from_file(file_path)

        return FileFilter()
