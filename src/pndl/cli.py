import argparse
import tempfile

from pathlib import Path

from .crawler import LinkIterator
from .writer import FileWriter
from .downloader import Aria2Downloader

OUTPUT_FILE = 'output.txt'
OUTPUT_ARIA2_FILE = 'output-aria2.txt'


def main():
    parser = argparse.ArgumentParser(description='Simple PhysioNet crawler & downloader')

    parser.add_argument('root_url',
                        help='URL to root directory of a PhysioNet archive')

    parser.add_argument('dir', nargs='?', type=Path,
                        help='Directory to store downloads')

    required_group = parser.add_argument_group('required arguments')
    optional_group = parser.add_argument_group('optional arguments')

    required_group.add_argument('-c', '--cookie-header', dest='header', required=True,
                                help='cookies header from PhysioNet')

    optional_group.add_argument('-o', '--output-text', action='store_true', dest='output_text',
                                help='Output crawl result to text file')

    optional_group.add_argument('-a', '--output-aria2', action='store_true', dest='output_aria2',
                                help='Output crawl result to destination as aria2 input file')
    optional_group.add_argument('-d', '--download', action='store_true',
                                help='Download crawled links using aria2 daemon via JSON-RPC')
    optional_group.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    options = {'header': args.header}
    aria2_options = {'dir': args.dir, **options}

    links = list(LinkIterator(args.root_url, args.verbose, options))

    if args.output_text:
        writer = FileWriter(args.root_url)
        writer.write_links_to_file(links, Path(OUTPUT_FILE))

    if args.output_aria2:
        writer = FileWriter(args.root_url, aria2_options)
        writer.write_links_to_file(links, Path(OUTPUT_ARIA2_FILE))

    if args.download:
        with tempfile.TemporaryDirectory() as tempdir:
            input_file = Path(OUTPUT_ARIA2_FILE)

            if not input_file.exists():
                input_file = Path(tempdir).joinpath(OUTPUT_ARIA2_FILE)
                writer = FileWriter(args.root_url, aria2_options)
                writer.write_links_to_file(links, input_file)

            downloader = Aria2Downloader(input_file)
            downloader.add_downloads()

