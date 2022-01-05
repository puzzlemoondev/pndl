# pndl

---
Simple PhysioNet crawler & downloader with [aria2](https://aria2.github.io/) support to accelerate download speed.
aria2 can run on remote server and use tools like [webui-aria2](https://github.com/ziahamza/webui-aria2) to monitor progress.

## Usage
```
usage: pndl [-h] -c HEADER [-o] [-a] [-d] [-v] root_url [dir]

Simple PhysioNet crawler & downloader

positional arguments:
  root_url              URL to root directory of a PhysioNet archive
  dir                   Directory to store downloads

options:
  -h, --help            show this help message and exit

required arguments:
  -c HEADER, --cookie-header HEADER
                        cookies header from PhysioNet

optional arguments:
  -o, --output-text     Output crawl result to text file
  -a, --output-aria2    Output crawl result to destination as aria2 input file
  -d, --download        Download crawled links using aria2 daemon via JSON-RPC
  -v, --verbose
```
## Dependencies
* wget
* aria2 daemon running for download

## Installation
```
poetry install
poetry run pndl
```
