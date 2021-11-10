import typing
import os
import os.path
import sys
import argparse
from lintlib import Linter


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description=("Utility for analyzing "
                     "compliance with the rules of writing code")
    )
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='description')

    file_parser = subparsers.add_parser('File',
                                        help='launching a linter for a file')

    # TODO helpMessage
    file_parser.add_argument('filename',
                             type=argparse.FileType(),
                             help="help message",
                             nargs='+')

    dir_parser = subparsers.add_parser('Dir',
                                       help='launching a linter for a dir')

    # TODO readable DIR + helpMessage
    dir_parser.add_argument('dirname',
                            type=str,
                            help="help message",
                            nargs='+')

    return parser.parse_args(sys.argv[1:])


def main():
    parser = create_argument_parser()
    if hasattr(parser, 'dirname'):
        for dir in parser.dirname:
            # TODO if условие для языка...
            for filename in os.listdir(dir):
                linter = Linter(filename=filename)
    else:
        for filename in parser.filename:
            linter = Linter(filename=filename)


if __name__ == "__main__":
    main()
