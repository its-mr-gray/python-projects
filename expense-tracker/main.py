from parsers import args, parser
from variables import COMMANDS

if __name__ == "__main__":
    handler = COMMANDS.get(args.command)

    if handler:
        handler(args)
    else:
        parser.print_help()
