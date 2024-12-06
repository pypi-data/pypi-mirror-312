from typing import Callable, Literal

from .utils import get_visible_length

Alignment = Literal["left", "center", "right"]


def center(text: str, width: int) -> str:
    """like text.center, but using visible length of text instead of len"""
    padding = width - get_visible_length(text)
    left_padding = int(padding / 2) + padding % 2
    right_padding = int(padding / 2) - padding % 2
    return " " * left_padding + text + " " * right_padding


def left(text: str, width: int) -> str:
    right_padding = (width - get_visible_length(text)) * " "
    return text + right_padding


def right(text: str, width: int) -> str:
    left_padding = (width - get_visible_length(text)) * " "
    return left_padding + text


def get_alignment_method(alignment: Alignment) -> Callable[[str, int], str]:
    return {
        "left": left,
        "right": right,
        "center": center,
    }[alignment]
