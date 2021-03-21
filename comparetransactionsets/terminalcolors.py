"""
Some ASNI escape codes for use in terminal output formatting.
See https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
"""

# Colors
_YELLOW = "\u001b[33m"

# Decorations
_BOLD = "\u001b[1m"

# Aliases
OK = _BOLD
RESET = "\u001b[0m"
WARNING = _YELLOW + _BOLD
