import responses

from .meta import standard_cli_test


@responses.activate
def test_makes_requests(capsys):
    standard_cli_test(
        cli_args_str="compare",
    )
