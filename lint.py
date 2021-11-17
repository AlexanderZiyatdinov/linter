import typing
import os
import os.path
import sys
import argparse
import io
from lintlib import Linter


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description=("Utility for analyzing "
                     "compliance with the rules of writing code")
    )
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='description')

    file_parser = subparsers.add_parser('files',
                                        help='launching a linter for a list of files')

    # TODO helpMessage
    file_parser.add_argument('filename',
                             type=argparse.FileType(),
                             help="help message",
                             nargs='+')

    dir_parser = subparsers.add_parser('dirs',
                                       help='launching a linter for list of dirs')

    # TODO readable DIR + helpMessage
    dir_parser.add_argument('dirname',
                            type=str,
                            help="help message",
                            nargs='+')

    return parser.parse_args(sys.argv[1:])


def iterate_through_files(collection: typing.Iterable, dirname=None):
    for file in collection:
        if isinstance(file, io.TextIOWrapper):
            linter = Linter(filename=file.name)
        else:
            linter = Linter(filename=os.path.join(dirname, file))
        linter.analyze()


def main():
    parser = create_argument_parser()
    if hasattr(parser, 'dirname'):
        for dir in parser.dirname:
            iterate_through_files(os.listdir(dir), dir)
    else:
        iterate_through_files(parser.filename)


if __name__ == "__main__":
    main()
