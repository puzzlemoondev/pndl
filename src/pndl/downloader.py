import aria2p

from pathlib import Path


class Aria2Downloader:
    def __init__(self, input_file: Path):
        self.input_file = input_file
        self._api = aria2p.API()

    def add_downloads(self):
        self._api.add(self.input_file.as_posix())
