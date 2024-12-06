import sys

from .transform import parse_context as parse

__version__ = "0.1.0"
__author__ = "King Jem <qqqqivy@gmail.com>"


def main():
    if len(sys.argv) == 2:
        sys.exit(parse(sys.argv[1],jsonify=True))
    else:
        curl_cmd = """ """.join(sys.argv[1:])
        sys.exit(parse(curl_cmd,jsonify=True))
