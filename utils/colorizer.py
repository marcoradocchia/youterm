class Colorize():
    global END
    END = '\33[0m'

    def style(input: str, style: str) -> str:
        # syles
        styles = {
            'cbold':     '\33[1m',
            'citalic':   '\33[3m',
            'curl':      '\33[4m',
            'cblink':    '\33[5m',
            'cblink2':   '\33[6m',
            'cselected': '\33[7m',
        }
        return styles[style] + input + END

    def fg(input: str, color: str) -> str:
        # fg colors
        colors = {
            'black':   '\33[30m',
            'red':     '\33[31m',
            'green':   '\33[32m',
            'yellow':  '\33[33m',
            'blue':    '\33[34m',
            'magenta': '\33[35m',
            'cyan':    '\33[36m',
            'white':   '\33[37m',
        }
        return colors[color] + input + END

    def bg(input: str, color: str) -> str:
        # bg colors
        colors = {
            'black':   '\33[40m',
            'red':     '\33[41m',
            'green':   '\33[42m',
            'yellow':  '\33[43m',
            'blue':    '\33[44m',
            'magenta': '\33[45m',
            'cyan':    '\33[46m',
            'white':   '\33[47m',
        }
        return colors[color] + input + END
