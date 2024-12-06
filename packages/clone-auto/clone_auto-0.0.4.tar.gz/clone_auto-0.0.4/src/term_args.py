""" Single function just to parse CLI args """

import argparse
import sys

from _version import __version__

def term_args() -> argparse.Namespace:
    """
    Analyzes sys.argv to map the text to options.

    Parameters
    ----------
    None

    Returns
    -------
    argparse.Namespace
        C struct in python where each member is an option. 
    """

    parser = argparse.ArgumentParser(
            prog="clone_auto",
            formatter_class=argparse.RawTextHelpFormatter,
            usage='%(prog)s [options]',
            description=
"""
Git Clone Public repositories from a given user
"""
)

    parser.add_argument(
            '-v','--version',
            action='version',
            version=f"""
%(prog)s v{__version__}
Copyright (C) 2024 Sivefunc
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by a human""")

    parser.add_argument(
            '-u', '--user',
            help="User whose repositories are going to be cloned.",
            type=str,
            metavar="[USER]",
            nargs=1,
            required=True
            )

    parser.add_argument(
            '--platforms',
            help="Platforms where the repos are located",
            metavar=None,
            type=str,
            nargs='+',
            choices=['gitlab', 'codeberg', 'github'],
            required=True
            )

    parser.add_argument(
            '--path',
            help="Path where the repos are going to be cloned",
            metavar=None,
            type=str,
            default="."
            )

    parser.add_argument(
            '-t', '--timeout',
            help="Time to wait for JSON response on platforms",
            metavar=None,
            type=float,
            default=10
            )

    # No arguments given, I just decided to leave it here.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args
