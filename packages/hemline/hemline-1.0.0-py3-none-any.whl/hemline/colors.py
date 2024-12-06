from enum import StrEnum


class Colors(StrEnum):
    BLACK = "\033[0;30m"
    DARK_RED = "\033[0;31m"
    DARK_GREEN = "\033[0;32m"
    BROWN = "\033[1;33m"
    DARK_BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    TEAL = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;90m"
    RED = "\033[0;92m"
    GREEN = "\033[0;92m"
    YELLOW = "\033[;93m"
    BLUE = "\033[0;94m"
    MAGENTA = "\033[;95m"
    CYAN = "\033[0;96m"
    WHITE = "\033[;97m"
    RESET = "\033[0m"


def colorize(text: str, color: Colors) -> str:
    return f"{color}{text}{Colors.RESET}"
