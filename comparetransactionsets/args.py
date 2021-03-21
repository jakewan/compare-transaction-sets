from argparse import ArgumentParser


def get_args(compare_fun, config_fun):
    parser = ArgumentParser(
        description=(
            "A command line utility to compare sets of transactions"
            " represented by rows from two sheets in Google Sheets"
        )
    )
    subparsers = parser.add_subparsers(required=True, dest="subcommand")
    compare_subparser = subparsers.add_parser("compare")
    compare_subparser.set_defaults(fn=compare_fun)
    _add_config_subcommand(subparsers, config_fun)
    return parser.parse_args()


def _add_config_subcommand(subparsers, config_fun):
    parser = subparsers.add_parser("config")
    parser.set_defaults(fn=config_fun)
    parsers = parser.add_subparsers(required=True, dest="config_subcommand")
    parsers.add_parser("init")
