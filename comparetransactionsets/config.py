import json
import sys
from os import makedirs
from os.path import dirname, exists, join

from appdirs import user_config_dir

from comparetransactionsets import __APP_NAME__, __AUTHOR__
from comparetransactionsets.terminalcolors import OK, RESET, WARNING

__CONFIG_FILE_PATH__ = join(
    user_config_dir(__APP_NAME__, __AUTHOR__),
    "config.json",
)

__DEFAULT_CONFIG__ = {"transaction-defs": []}


def init_config_file(args):
    if exists(__CONFIG_FILE_PATH__):
        sys.exit(
            (
                f"{WARNING}A configuration file already"
                f" exists at {__CONFIG_FILE_PATH__}.{RESET}"
            )
        )
    makedirs(dirname(__CONFIG_FILE_PATH__), exist_ok=True)
    _write_config(__DEFAULT_CONFIG__)
    print(f"{OK}Configuration file written to: {__CONFIG_FILE_PATH__}{RESET}")


def read():
    """Read from the configuration file and return the result."""
    return _read_config()


def _read_config():
    try:
        with open(__CONFIG_FILE_PATH__) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(
            (
                f"{WARNING}No configuration file found at {__CONFIG_FILE_PATH__}.\n"
                f"Please run `{__APP_NAME__} config init`"
                f" to generate one.{RESET}"
            )
        )


def _write_config(config):
    with open(__CONFIG_FILE_PATH__, "w") as f:
        _json_dump(config, f)


def _json_dump(obj, fp):
    json.dump(obj, fp, sort_keys=True, indent=4)
