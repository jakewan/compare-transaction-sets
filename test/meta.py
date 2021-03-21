import json
import sys
from contextlib import contextmanager
from io import StringIO
from os import makedirs
from os.path import join
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

import comparetransactionsets.config
from comparetransactionsets import __APP_NAME__, cli

__DEFAULT_CONFIG__ = {"foo": "bar"}


class TempConfigFile(TemporaryDirectory):
    def __init__(self, init_file=True, init_dir=False, config_obj=None):
        super().__init__()
        parent_dir = join(self.name, "subdir")
        if init_file or init_dir:
            makedirs(parent_dir)
        if init_file:
            with open(join(parent_dir, "config.json"), "w") as f:
                json.dump(config_obj, f)


def standard_cli_test(
    cli_args=None,
    cli_args_str=None,
    temp_config_file_args={"config_obj": __DEFAULT_CONFIG__},
    assert_fun=None,
    assert_config_fun=None,
    expected_exception_type=None,
    assert_excinfo_fun=None,
    user_inputs=[],
):
    assert (
        cli_args is not None or cli_args_str is not None
    ), "The caller must supply the cli_args or cli_args_str argument."
    cli_args = cli_args if cli_args_str is None else cli_args_str.split()
    with TempConfigFile(**temp_config_file_args) as tempdir_name:
        config_file_path = join(tempdir_name, "subdir/config.json")
        with patch.object(
            comparetransactionsets.config, "__CONFIG_FILE_PATH__", config_file_path
        ):
            # As a convenience, allow caller to omit the program name.
            if cli_args[0] != __APP_NAME__:
                cli_args[0:0] = [__APP_NAME__]
            with patch.object(sys, "argv", cli_args), replace_stdin(
                StringIO("\n".join(user_inputs))
            ):
                if expected_exception_type is not None:
                    with pytest.raises(expected_exception_type) as excinfo:
                        cli.main()
                    if assert_excinfo_fun is not None:
                        assert_excinfo_fun(excinfo)
                else:
                    cli.main()
        if assert_config_fun is not None:
            assert_config_fun(config_file_path)
    if assert_fun is not None:
        assert_fun(config_file_path=config_file_path)


def make_assert_config_fun(expected_config):
    def _inner(config_file_path):
        with open(config_file_path) as f:
            resulting_config = json.load(f)
        assert resulting_config == expected_config

    return _inner


@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig
