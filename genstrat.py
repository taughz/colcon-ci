#!/usr/bin/env python3

import argparse
import json
import sys


DEFAULT_OS = ("macos-latest", "ubuntu-22.04", "windows-latest")
DEFAULT_PYTHON = ("3.8", "3.9", "3.10", "3.11", "3.12")

PY36_JSON = '{ "os": "ubuntu-20.04", "python": "3.6" }'
STDEB_JSON = '{ "os": "ubuntu-22.04", "stdeb-check": "1" }'


def yes_no_to_bool(yes_no):
    assert yes_no in ["yes", "no"]
    return yes_no == "yes"


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--os",
        nargs="+",
        action="extend",
        help=f"matrix OSs (default: {' '.join(DEFAULT_OS)})",
    )
    parser.add_argument(
        "--python",
        nargs="+",
        action="extend",
        help=f"matrix Python versions (default: {' '.join(DEFAULT_PYTHON)})",
    )
    parser.add_argument(
        "-i",
        "--include",
        action="append",
        help="include some arbitrary section (default: '')",
    )
    parser.add_argument(
        "--include-py36",
        choices=["yes", "no"],
        default="yes",
        help="include the Python 3.6 section (default: yes)",
    )
    parser.add_argument(
        "--include-stdeb",
        choices=["yes", "no"],
        default="yes",
        help="include the stdeb section (default: yes)",
    )
    return parser


def parse_args(argv):
    parser = get_parser()
    args = parser.parse_args(argv)
    if args.os is None:
        args.os = list(DEFAULT_OS)
    if args.python is None:
        args.python = list(DEFAULT_PYTHON)
    if args.include is None:
        args.include = []
    if yes_no_to_bool(args.include_py36):
        args.include.append(PY36_JSON)
    if yes_no_to_bool(args.include_stdeb):
        args.include.append(STDEB_JSON)
    return args


def main(argv):
    args = parse_args(argv)
    strategy = {"matrix": {"os": args.os, "python": args.python, "include": []}}
    for inc in args.include:
        try:
            strategy["matrix"]["include"].append(json.loads(inc))
        except json.JSONDecodeError:
            print(f"ERROR: Failed to parse: {repr(inc)}", file=sys.stderr)
            return 1
    print(json.dumps(strategy))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
