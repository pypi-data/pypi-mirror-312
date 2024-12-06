from os import get_terminal_size
from re import compile as re_compile


def get_terminal_width() -> int:  # pragma: no cover
    return get_terminal_size().columns


_ANSI_ESCAPE = re_compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")


def get_visible_length(text: str) -> int:  # pragma: no cover
    """Length of string but ignoring terminal color code escape sequences"""
    return len(_ANSI_ESCAPE.sub("", text))
