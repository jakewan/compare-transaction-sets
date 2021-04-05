import locale
from decimal import Decimal


class MismatchedValue:
    def __init__(self, date, from_value, to_value):
        self.__date = date
        self.__from_value = Decimal(self._string_to_decimal(from_value))
        self.__to_value = Decimal(self._string_to_decimal(to_value))

    @property
    def date(self):
        return self.__date

    @property
    def from_value(self):
        return self.__from_value

    @property
    def to_value(self):
        return self.__to_value

    @staticmethod
    def _string_to_decimal(str_val):
        db = locale.localeconv()
        return str_val.replace(db["currency_symbol"], "").replace(
            db["mon_thousands_sep"], ""
        )
