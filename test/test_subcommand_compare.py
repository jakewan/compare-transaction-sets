from unittest.mock import patch

import comparetransactionsets.compare
from comparetransactionsets.terminalcolors import OK, RESET, WARNING

from .meta import standard_cli_test


def _default(temp_config_obj, return_data):
    def _execute():
        result = return_data[_execute.idx]
        _execute.idx += 1
        return result

    _execute.idx = 0

    with patch.object(
        comparetransactionsets.compare, "_get_creds"
    ) as _get_creds, patch.object(comparetransactionsets.compare, "build") as build:
        _get_creds.return_value = "blah _get_creds"
        spreadsheets = build.return_value.spreadsheets
        values = spreadsheets.return_value.values
        get = values.return_value.get
        execute = get.return_value.execute
        execute.side_effect = _execute
        return standard_cli_test(
            cli_args_str="compare",
            temp_config_obj=temp_config_obj,
        )


def test_finds_diff_in_values(capsys):
    temp_config_obj = {
        "spreadsheets": {
            "spreadsheet1": {"spreadsheetId": "some-sheet-1"},
            "spreadsheet2": {"spreadsheetId": "some-sheet-2"},
        },
        "viewProfiles": {
            "spreadsheet1View": {
                "spreadsheet": "spreadsheet1",
                "dateColumn": "Date",
                "filter": ["Name", "Description"],
            },
            "spreadsheet2View": {
                "spreadsheet": "spreadsheet2",
                "dateColumn": "Date",
                "filter": ["Name", "Comment"],
            },
        },
        "views": {
            "Foo Withdrawals": {
                "profile": "spreadsheet1View",
                "sheet": "Foo Data",
                "valueColumn": "Withdrawal",
            },
            "Baz Deposits": {
                "profile": "spreadsheet2View",
                "sheet": "Baz Data",
                "valueColumn": "Deposit",
            },
        },
        "series": {
            "Foo to Baz": {
                "from": {
                    "view": "Foo Withdrawals",
                    "filter": ["Baz", "Some description"],
                },
                "to": {
                    "view": "Baz Deposits",
                    "filter": ["Foo", "Some comment"],
                },
            }
        },
    }
    api_values = (
        {
            "values": [
                ["Date", "Name", "Description", "Deposit", "Withdrawal"],
                ["2/10/2021", "Baz", "Some description", "", "$100.00"],
            ]
        },
        {
            "values": [
                ["Date", "Name", "Comment", "Deposit", "Withdrawal"],
                ["2/10/2021", "Foo", "Some comment", "$1,000.01", ""],
            ]
        },
    )
    _default(temp_config_obj, api_values)

    # Verify
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"""{WARNING}We found the following problems:{RESET}

For transaction series "Foo to Baz":

* Transaction on 2/10/2021 with mismatched values:

    From value:   $100.00
      To value: $1,000.01

"""
    )


def test_find_mismatched_transactions(capsys):
    temp_config_obj = {
        "spreadsheets": {
            "spreadsheet1": {"spreadsheetId": "some-sheet-1"},
            "spreadsheet2": {"spreadsheetId": "some-sheet-2"},
        },
        "viewProfiles": {
            "spreadsheet1View": {
                "spreadsheet": "spreadsheet1",
                "dateColumn": "Date",
                "filter": ["Name", "Description"],
            },
        },
        "views": {
            "Foo Withdrawals": {
                "profile": "spreadsheet1View",
                "sheet": "Foo Data",
                "valueColumn": "Withdrawal",
            },
            "Bar Deposits": {
                "profile": "spreadsheet1View",
                "sheet": "Bar Data",
                "valueColumn": "Deposit",
            },
        },
        "series": {
            "Foo to Bar": {
                "from": {
                    "view": "Foo Withdrawals",
                    "filter": ["Bar", "Some description"],
                },
                "to": {
                    "view": "Bar Deposits",
                    "filter": ["Foo", "Some description"],
                },
            }
        },
    }
    api_values = (
        {
            "values": [
                ["Date", "Name", "Description", "Deposit", "Withdrawal"],
                ["2/10/2021", "Bar", "Some description", "", "$1,000.01"],
            ]
        },
        {
            "values": [
                ["Date", "Name", "Description", "Deposit", "Withdrawal"],
                ["2/11/2021", "Foo", "Some description", "$1,000.01", ""],
            ]
        },
    )
    _default(temp_config_obj, api_values)

    # Verify
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"""{WARNING}We found the following problems:{RESET}

For transaction series "Foo to Bar":

* Withdrawals from "Foo Data" not matched by deposit to "Bar Data":

    2/10/2021 | Bar | Some description | $1,000.01

* Deposits to "Bar Data" not matched by withdrawal from "Foo Data":

    2/11/2021 | Foo | Some description | $1,000.01

"""
    )


def test_similar_filter_for_opposing_transaction_defs_is_okay(capsys):
    temp_config_obj = {
        "spreadsheets": {
            "spreadsheet1": {"spreadsheetId": "some-sheet-1"},
            "spreadsheet2": {"spreadsheetId": "some-sheet-2"},
        },
        "viewProfiles": {
            "spreadsheet1View": {
                "spreadsheet": "spreadsheet1",
                "dateColumn": "Date",
                "filter": ["Column1", "Column2"],
            },
            "spreadsheet2View": {
                "spreadsheet": "spreadsheet2",
                "dateColumn": "Date",
                "filter": ["Column1", "Column2"],
            },
        },
        "views": {
            "Foo Withdrawals": {
                "profile": "spreadsheet1View",
                "sheet": "Foo Data",
                "valueColumn": "Withdrawal",
            },
            "Baz Deposits": {
                "profile": "spreadsheet2View",
                "sheet": "Baz Data",
                "valueColumn": "Deposit",
            },
        },
        "series": {
            "Foo to Baz": {
                "from": {
                    "view": "Foo Withdrawals",
                    "filter": ["Baz", "Same on both sides"],
                },
                "to": {
                    "view": "Baz Deposits",
                    "filter": ["Foo", "Same on both sides"],
                },
            }
        },
    }
    api_values = (
        {
            "values": [
                ["Date", "Column1", "Column2", "Deposit", "Withdrawal"],
                ["2/10/2021", "Baz", "Same on both sides", "", "$100.00"],
                # We don't expect a matching transaction part for this row
                # because there is no transaction definition configured in
                # that direction.
                ["2/11/2021", "Baz", "Same on both sides", "$15.00", ""],
            ]
        },
        {
            "values": [
                ["Date", "Column1", "Column2", "Deposit", "Withdrawal"],
                ["2/10/2021", "Foo", "Same on both sides", "$100.00", ""],
            ]
        },
    )
    _default(temp_config_obj, api_values)

    # Verify
    captured = capsys.readouterr()
    assert (
        captured.out
        == f"""{OK}No problems found.{RESET}
"""
    )


def test_second_descriptive_column_value_config_is_optional():
    temp_config_obj = {
        "spreadsheets": {
            "foo": {"spreadsheetId": "foo"},
        },
        "viewProfiles": {
            "foo": {
                "spreadsheet": "foo",
                "dateColumn": "Date",
                "filter": ["Column1", "Column2"],
            },
        },
        "views": {
            "Foo": {
                "profile": "foo",
                "sheet": "Foo",
                "valueColumn": "Withdrawal",
            },
            "Bar": {
                "profile": "foo",
                "sheet": "Bar",
                "valueColumn": "Deposit",
            },
        },
        "series": {
            "Foo to Bar": {
                "from": {
                    "view": "Foo",
                    "filter": ["Bar"],
                },
                "to": {
                    "view": "Bar",
                    "filter": ["Foo"],
                },
            }
        },
    }
    api_values = (
        {
            "values": [
                ["Date", "Column1", "Column2", "Deposit", "Withdrawal"],
                ["2/10/2021", "Bar", "", "", "$100.00"],
                ["2/11/2021", "Bar", "", "", "$15.00"],
            ]
        },
        {
            "values": [
                ["Date", "Column1", "Column2", "Deposit", "Withdrawal"],
                ["2/10/2021", "Foo", "", "$100.00", ""],
                ["2/11/2021", "Foo", "", "$15.00", ""],
            ]
        },
    )
    _default(temp_config_obj, api_values)
