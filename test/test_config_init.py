from comparetransactionsets.terminalcolors import OK, RESET

from .meta import make_assert_config_fun, standard_cli_test

__EXPECTED_DEFAULT_CONFIG__ = {"transaction-defs": []}


def test_writes_expected_default_config():
    standard_cli_test(
        cli_args_str="config init",
        init_file=False,
        assert_config_fun=make_assert_config_fun(__EXPECTED_DEFAULT_CONFIG__),
    )


def test_displays_config_file_location(capsys):
    def _assert(config_file_path):
        captured = capsys.readouterr()
        assert (
            captured.out
            == f"{OK}Configuration file written to: {config_file_path}{RESET}\n"
        )

    standard_cli_test(
        cli_args_str="config init",
        init_file=False,
        assert_fun=_assert,
    )


def test_aborts_config_init_if_file_exists():
    standard_cli_test(
        cli_args_str="config init",
        expected_exception_type=SystemExit,
    )
