# youterm: CLI tool to search for YouTube videos and play selected video/audio
# via MPV
# Copyright (C) 2022 Marco Radocchia
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see https://www.gnu.org/licenses/.

from os import get_terminal_size
from youterm.colorizer import Colorize


def wrap(input: str, pref_len: int, color: str) -> str:
    fg = Colorize.fg
    cols, _ = get_terminal_size()
    cols -= pref_len  # 4 cols are already used by lines
    new_string = []
    divisions = int(len(input) / cols)
    if divisions == 0:
        return fg(input=input, color=color)
    for index in range(divisions + 1):
        split = input[:cols]
        if index < divisions:
            new_string.append(fg(input=split, color=color) + "\n│   │   ")
        else:
            new_string.append(fg(input=split, color=color))
        input = input[cols:]
    return "".join(new_string)
