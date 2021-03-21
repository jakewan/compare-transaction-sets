import comparetransactionsets
from comparetransactionsets.args import get_args
from comparetransactionsets.compare import exec as _compare


def main():
    # Parse user input and validate arguments
    args = get_args(_compare, _config)
    args.fn(args)


def _config(args):
    {"init": comparetransactionsets.config.init_config_file}[args.config_subcommand](
        args
    )
