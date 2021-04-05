import locale
from datetime import date
from functools import partial
from itertools import filterfalse

from googleapiclient.discovery import build

import comparetransactionsets.config
from comparetransactionsets import OK, RESET, WARNING
from comparetransactionsets.diffset import DiffSet
from comparetransactionsets.get_creds import exec as _get_creds
from comparetransactionsets.mismatchedtransaction import MismatchedTransaction
from comparetransactionsets.mismatchedvalue import MismatchedValue
from comparetransactionsets.transactiondefinition import TransactionDefinition
from comparetransactionsets.transactiondirection import TransactionDirection

locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))


def _get_mismatched_values(defn, from_values, to_values):
    direction = TransactionDirection("from", defn)
    col_name_left_date = direction.get_left_date_column()
    col_name_right_date = direction.get_right_date_column()
    col_name_left_value = direction.get_left_value_column()
    col_name_right_value = direction.get_right_value_column()
    for i in from_values:
        for j in filterfalse(_is_found, to_values):
            if i[col_name_left_date] == j[col_name_right_date]:
                if i[col_name_left_value] != j[col_name_right_value]:
                    # Mark both of these objects as "found", so later processing can
                    # ignore them.
                    i["__found"] = j["__found"] = True
                    yield MismatchedValue(
                        i[col_name_left_date],
                        i[col_name_left_value],
                        j[col_name_right_value],
                    )


def _is_found(obj):
    try:
        return obj["__found"] is True
    except KeyError:
        return False


def _get_mismatched_transaction_parts(transaction_direction, left_values, right_values):
    col_name_left_date = transaction_direction.get_left_date_column()
    col_name_right_date = transaction_direction.get_right_date_column()
    col_name_left_1 = transaction_direction.get_left_column_name(0)
    col_name_left_2 = transaction_direction.get_left_column_name(1)
    col_name_left_value = transaction_direction.get_left_value_column()
    col_name_right_value = transaction_direction.get_right_value_column()

    for i in filter(
        transaction_direction._is_left_match, filterfalse(_is_found, left_values)
    ):
        found = False
        for j in filter(
            transaction_direction._is_right_match, filterfalse(_is_found, right_values)
        ):
            if (
                i[col_name_left_date] == j[col_name_right_date]
                and i[col_name_left_value] == j[col_name_right_value]
            ):
                found = True
                j["__found"] = True
                break
        if not found:
            yield MismatchedTransaction(
                i[col_name_left_date],
                i[col_name_left_1],
                i[col_name_left_2],
                i[col_name_left_value],
            )


def _get_date_field(date_col_name):
    def _inner(obj):
        date_parts = obj[date_col_name].split("/")
        return date(int(date_parts[2]), int(date_parts[0]), int(date_parts[1]))

    return _inner


def _compare_set(defn, sheets_service):
    def _result_to_dicts(raw_result):
        result = []
        values = raw_result["values"]
        column_names = values[0]
        for i in raw_result["values"][1:]:
            dict_value = {}
            for column_idx, column_name in enumerate(column_names):
                dict_value[column_name] = i[column_idx]
            result.append(dict_value)
        return result

    def _filter_row(val, test):
        if val[test["columnName"]] == test["value"]:
            return True
        return False

    def _filter(defn, values):
        result = []
        for i in values:
            if i[defn.value_column] == "":
                continue
            ok = True
            for filter_test in defn.filter:
                if not _filter_row(i, filter_test):
                    ok = False
                    break
            if ok:
                result.append(i)
        return result

    result = (
        sheets_service.values()
        .get(
            spreadsheetId=defn.from_def.spreadsheet_id,
            range=f"{defn.from_def.sheet_name}!{defn.from_def.range}",
        )
        .execute()
    )
    from_values = sorted(
        _filter(defn.from_def, _result_to_dicts(result)),
        key=_get_date_field(defn.from_def.date_column),
    )
    result = (
        sheets_service.values()
        .get(
            spreadsheetId=defn.to_def.spreadsheet_id,
            range=f"{defn.to_def.sheet_name}!{defn.to_def.range}",
        )
        .execute()
    )
    to_values = sorted(
        _filter(defn.to_def, _result_to_dicts(result)),
        key=_get_date_field(defn.to_def.date_column),
    )
    result = DiffSet(defn)
    for i in _get_mismatched_values(defn, from_values, to_values):
        result.mismatched_values.append(i)
    for i in _get_mismatched_transaction_parts(
        TransactionDirection("from", defn), from_values, to_values
    ):
        result.mismatched_withdrawals.append(i)
    for i in _get_mismatched_transaction_parts(
        TransactionDirection("to", defn), to_values, from_values
    ):
        result.mismatched_deposits.append(i)
    return result


def exec(args):
    _to_currency_string = partial(locale.currency, grouping=True)

    def _normalize_value(first, second):
        first_formatted = _to_currency_string(first)
        second_formatted = _to_currency_string(second)
        return str.rjust(
            first_formatted, max(len(first_formatted), len(second_formatted))
        )

    def _get_diff_line(diff):
        parts = [diff.date, diff.name, diff.description, diff.value]
        return f"    {' | '.join(parts)}"

    config = comparetransactionsets.config.read()
    creds = _get_creds()
    service = build("sheets", "v4", credentials=creds)
    sheets = service.spreadsheets()
    diffs = [
        _compare_set(defn, sheets)
        for defn in (TransactionDefinition(i) for i in config["transactionDefs"])
    ]
    diffs = list(filter(lambda x: x.contains_mismatches, diffs))
    if len(diffs) < 1:
        print(f"{OK}No problems found.{RESET}")
        return

    print(f"{WARNING}We found the following problems:{RESET}")

    for series_diff_set in diffs:
        print()
        print(f'For transaction series "{series_diff_set.series_name}":')
        if 0 < len(series_diff_set.mismatched_withdrawals):
            print()
            print(
                f'* Withdrawals from "{series_diff_set.from_def.sheet_name}"'
                f' not matched by deposit to "{series_diff_set.to_def.sheet_name}":'
            )
            for diff in series_diff_set.mismatched_withdrawals:
                print()
                print(_get_diff_line(diff))

        if 0 < len(series_diff_set.mismatched_deposits):
            print()
            print(
                f'* Deposits to "{series_diff_set.to_def.sheet_name}" not'
                f' matched by withdrawal from "{series_diff_set.from_def.sheet_name}":'
            )
            for diff in series_diff_set.mismatched_deposits:
                print()
                print(_get_diff_line(diff))

        for diff in series_diff_set.mismatched_values:
            print()
            print(f"* Transaction on {diff.date} with mismatched values:")
            print()
            print(f"    From value: {_normalize_value(diff.from_value, diff.to_value)}")
            print(f"      To value: {_normalize_value(diff.to_value, diff.from_value)}")
    print()
