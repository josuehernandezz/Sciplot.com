def plotColors(pallete: dict, file_length: int) -> list[str]:
    if file_length in [1, 2]:
        color = pallete[3]
        if file_length == 1:
            color = color[:-2]
            return color
        else:
            color = color[:-1]
            return color
    else:
        color = pallete[file_length]
        return color

def determine_delimiter(file_content):
    # with open(file_content, 'r') as file:
    #     first_line = file.readline()
    first_line = file_content.splitlines()[0]
    if '\t' in first_line:
        print('delimiter is "\ t"')
        return '\t'  # Tab delimiter
    elif ',' in first_line:
        print('delimiter is ","')
        return ','  # Comma delimiter
    elif ';' in first_line:
        print('delimiter is ";"')
        return ';'  # Semicolon delimiter
    elif '\r' in first_line:
        print('delimiter is "\ r"')
        return '\r'  # Semicolon delimiter
    else:
        print('delimiter is space')
        return ' '  # Space delimiter (default)

def det_delim_ex(file_content):
    with open(file_content, 'r') as file:
        first_line = file.readline()
    # first_line = file_content.splitlines()[0]
    if '\t' in first_line:
        print('delimiter is "\ t"')
        return '\t'  # Tab delimiter
    elif ',' in first_line:
        print('delimiter is ","')
        return ','  # Comma delimiter
    elif ';' in first_line:
        print('delimiter is ";"')
        return ';'  # Semicolon delimiter
    elif '\r' in first_line:
        print('delimiter is "\ r"')
        return '\r'  # Semicolon delimiter
    else:
        print('delimiter is space')
        return ' '  # Space delimiter (default)
