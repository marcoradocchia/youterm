from os import get_terminal_size

def wrapper(input: str, prefix_length: int) -> str:
    cols, _ = get_terminal_size()
    cols -= prefix_length # 4 cols are already used by lines
    new_string = []
    divisions = int(len(input) / cols)
    if divisions == 0: return input
    for index in range(divisions+1):
        split = input[:cols]
        if index < divisions:
            new_string.append(split + "\n│   │   ")
        else:
            new_string.append(split)
        input = input[cols:]
    return ''.join(new_string)
