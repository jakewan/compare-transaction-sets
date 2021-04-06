from datetime import date

__APP_NAME__ = "compare-transaction-sets"
__AUTHOR__ = "Jacob Wan"

# Colors
_YELLOW = "\u001b[33m"

# Decorations
_BOLD = "\u001b[1m"

# Aliases
OK = _BOLD
RESET = "\u001b[0m"
WARNING = _YELLOW + _BOLD


def parse_date(val):
    parts = val.split("/")
    return date(int(parts[2]), int(parts[0]), int(parts[1]))
