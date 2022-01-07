from os import get_terminal_size
from .colorizer import Colorize


def wrap(input: str, pref_len: int, color: str) -> str:
    fg = Colorize.fg
    cols, _ = get_terminal_size()
    cols -= pref_len  # 4 cols are already used by lines
    new_string = []
    divisions = int(len(input) / cols)
    if divisions == 0:
        return fg(input=input, color=color)
    for index in range(divisions+1):
        split = input[:cols]
        if index < divisions:
            new_string.append(fg(input=split, color=color) + "\n│   │   ")
        else:
            new_string.append(fg(input=split, color=color))
        input = input[cols:]
    return ''.join(new_string)
