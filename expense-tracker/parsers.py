"""
parsers.py

contains all the argument parsing for the CLI
"""

from argparse import ArgumentParser

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)

# require certain args only for add cmd
add_parser = subparsers.add_parser(name="add")
add_parser.add_argument(
    "-d", "--description", required=True, help="description of the expense"
)
add_parser.add_argument(
    "-a", "--amount", type=float, required=True, help="the amount of the expense"
)
add_parser.add_argument(
    "-c", "--category", required=True, help="the category of the expense"
)

view_parser = subparsers.add_parser(name="view")

summary_parser = subparsers.add_parser(name="summary")
summary_parser.add_argument(
    "-m",
    "--monthly",
    type=int,
    help="view a summary of expenses for a given integer month (limited to the current calendar year)",
)
summary_parser.add_argument(
    "-c", "--category", help="view a summary of expenses from a given category"
)

update_parser = subparsers.add_parser(name="update")
update_parser.add_argument("id", help="ID of the expense to update")
update_parser.add_argument("-d", "--description", help="edit the expense description")
update_parser.add_argument("-a", "--amount", type=float, help="edit the expense amount")
update_parser.add_argument("-c", "--category", help="edit the expense category")

remove_parser = subparsers.add_parser(name="remove")
remove_parser.add_argument("id", help="ID of the expense to remove")

export_parser = subparsers.add_parser(name="export")

args = parser.parse_args()
