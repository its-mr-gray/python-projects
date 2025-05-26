"""
parsers.py

contains the argument parsers for the CLI application
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "username", metavar="username", help="enter a username to see activity"
)
args = parser.parse_args()
