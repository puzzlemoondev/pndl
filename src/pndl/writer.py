from pathlib import Path


class FileWriter:
    def __init__(self, root_url: str, aria2_options=None):
        if aria2_options is None:
            aria2_options = dict()

        self.root_url = root_url
        self.aria2_options = aria2_options

    def write_links_to_file(self, links: iter, file):
        lines = self._get_lines(links)

        with open(file, 'w') as f:
            f.writelines(line + '\n' for line in lines)

    def _get_lines(self, links: iter):
        for link in links:
            download_link = link + '?download'
            yield download_link

            if header := self.aria2_options.get('header'):
                yield f' header={header}'

            if output_dir := self.aria2_options.get('dir'):
                if output_dir := self._resolve_output_dir(link, output_dir):
                    yield f' dir={output_dir}'

    def _resolve_output_dir(self, link: str, output_dir: Path):
        file_path = link.replace(self.root_url, '')

        *directories, _ = file_path.split('/')
        output_file_dir = output_dir.joinpath(*directories).as_posix()

        return output_file_dir
