import subprocess

from itertools import groupby
from lxml import html


class LinkIterator:
    def __init__(self, root_url: str, verbose: bool, options: dict):
        self.root_url = root_url
        self.verbose = verbose
        self.options = options

    def __iter__(self):
        for link in self._get_links(self.root_url):
            if self.verbose:
                print(link)
            yield link

    def _get_links(self, url: str):
        root = self._request(url)
        doc = html.fromstring(root)
        hrefs = (link[2] for link in doc.iterlinks())
        directories, files = LinkIterator._partition_directories(hrefs)

        yield from (url + file for file in files)

        for directory in directories:
            directory_url = url + directory
            yield from self._get_links(directory_url)

    def _request(self, url: str):
        command = f'wget -qO- {url}'

        for key, value in self.options.items():
            command += f' --{key} "{value}"'

        output = subprocess.run(command, shell=True, capture_output=True)

        return output.stdout

    @staticmethod
    def _partition_directories(paths: iter):
        directories = []
        files = []

        for is_directory, group in groupby(paths, lambda x: x.endswith('/')):
            if is_directory:
                directories.extend(filter(lambda x: x != '../', group))
            else:
                files.extend(group)

        return directories, files
