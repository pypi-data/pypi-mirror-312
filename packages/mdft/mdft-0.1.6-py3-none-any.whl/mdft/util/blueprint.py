from mdft.file import File

from .options import Options


class Blueprint:
    options: Options
    file: File

    def __init__(self, file: File, options: Options):
        self.options = options
        self.file = file
