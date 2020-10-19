from typing import Tuple, Union


class Color:

    """
    A composable coloring object.

    RED = Color(91)
    RED_FOREGROUND = RED
    BLUE_BACKGROUND = Color(104)

    # Sum Colors to combine them:
    RED_FORE_BLUE_BACK = RED_FOREGROUND + BLUE_BACKGROUND

    # Apply it to strings about to be printed
    >>> print(RED @ 'text') will color the text in red, and reset the color afterwards;
    >>> print(RED('text')) also works;
    >>> print(f'{RED}text{RESET}') doing it this way requires you to reset the color yourself;
    >>> print(RED_FG @ BLUE_BG @ 'text') Combine them on the spot;

    See more examples in test_color.py.

    Most color aliases can already found as consts in this module, + in Fore & Back.

    """

    codes: Tuple[int, ...]

    def __init__(self, *codes: int):
        self.codes = codes

    def __str__(self):
        return f'\033[{";".join(map(str, self.codes))}m'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Color(*self.codes, *other.codes)
        return other + str(self)

    def __call__(self, item: Union[str, 'Color']) -> Union[str, 'Color']:
        if isinstance(item, self.__class__):
            return self + item
        return self.colorize(item)

    def colorize(self, text: str) -> str:
        return str(self) + text + '\033[m'

    def __rmatmul__(self, item):
        return self(item)

    def __matmul__(self, item):
        return self(item)

    def __repr__(self):
        return f'{self.__class__.__name__}(codes={self.codes})'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.codes == other.codes
        return False


class Fore:
    """Foreground colors."""
    RED = Color(91)
    GREEN = Color(92)
    YELLOW = Color(93)
    BLUE = Color(94)
    MAGENTA = Color(95)
    CYAN = Color(96)
    RESET = Color(39)


class Back:
    """Background colors."""
    RED = Color(101)
    GREEN = Color(102)
    YELLOW = Color(103)
    BLUE = Color(104)
    MAGENTA = Color(105)
    CYAN = Color(106)
    RESET = Color(49)


class Style:
    RESET = Color(22)
    BRIGHT = Color(1)


RESET_ALL = Color()
INVERT = Color(7)
