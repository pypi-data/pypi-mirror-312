from .alignment import Alignment
from .colors import colorize
from .themes import single

DEFAULT_THEME = single
DEFAULT_TEXT_ALIGNMENT: Alignment = "left"
DEFAULT_FRAME_ALIGNMENT: Alignment = "center"
DEFAULT_HORIZONTAL_PADDING = 4
DEFAULT_VERTICAL_PADDING = 1
DEFAULT_COLORIZE = colorize
DEFAULT_OUTER_WIDTH = 88 + 2 * DEFAULT_HORIZONTAL_PADDING + 2
