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

class Colorize:
    global END
    END = "\33[0m"

    def style(input: str, style: str) -> str:
        # syles
        styles = {
            "bold": "\33[1m",
            "italic": "\33[3m",
            "bolditalic": "\33[1m\33[3m",
            "url": "\33[4m",
            "blink": "\33[5m",
            "blink2": "\33[6m",
            "selected": "\33[7m",
        }
        return styles[style] + input + END

    def fg(input: str, color: str) -> str:
        # fg colors
        colors = {
            "black": "\33[30m",
            "red": "\33[31m",
            "green": "\33[32m",
            "yellow": "\33[33m",
            "blue": "\33[34m",
            "magenta": "\33[35m",
            "cyan": "\33[36m",
            "white": "\33[37m",
        }
        return colors[color] + input + END

    def bg(input: str, color: str) -> str:
        # bg colors
        colors = {
            "black": "\33[40m",
            "red": "\33[41m",
            "green": "\33[42m",
            "yellow": "\33[43m",
            "blue": "\33[44m",
            "magenta": "\33[45m",
            "cyan": "\33[46m",
            "white": "\33[47m",
        }
        return colors[color] + input + END
