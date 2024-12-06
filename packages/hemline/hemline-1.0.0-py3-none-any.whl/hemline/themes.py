from dataclasses import dataclass


@dataclass()
class Theme:
    horizontal: str
    vertical: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str

    def __post_init__(self) -> None:
        for field in [
            "horizontal",
            "vertical",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
        ]:
            border = self.__validate_border(field)
            setattr(self, field, border)

    def __validate_border(self, field: str) -> str:
        border = getattr(self, field)
        if not isinstance(border, str):
            raise TypeError(f"Delimiter border `{field}` must be a string.")

        length = len(border)
        if not length == 1:
            raise ValueError(
                "Delimiters must be single characters. "
                f'`{field}` ("{border}") has {length}.'
            )
        return border


def factory(character: str, corner: str | None = None) -> Theme:
    corner = corner or character
    return Theme(
        horizontal=character,
        vertical=character,
        top_left=corner,
        top_right=corner,
        bottom_left=corner,
        bottom_right=corner,
    )


single: Theme = Theme(
    horizontal="─",
    vertical="│",
    top_left="┌",
    top_right="┐",
    bottom_left="└",
    bottom_right="┘",
)
double: Theme = Theme(
    horizontal="═",
    vertical="║",
    top_left="╔",
    top_right="╗",
    bottom_left="╚",
    bottom_right="╝",
)
dotted = factory("·")
none = factory(" ")
