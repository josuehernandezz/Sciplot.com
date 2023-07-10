import pandas as pd

def grab_lines(file) -> list:
    file.seek(0)    
    lines = [line.decode() for line in file.readlines()]
    return lines

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def grab_nums(lines: list) -> list[float]:
    '''
    Takes a list of lines, and tests items in each line that are convertable to a float, 
    
    if any item in line is not convertable, the line is discarded.
    
    '''
    nums = []  # list to hold numbers from the text file
    for line in lines:
        split_line = line.split()  # remove white space from each line and split into a list
        if split_line and all(is_float(element) for element in split_line):
            nums.append([float(element) for element in split_line])
    return nums

def nums2df(nums: list[float]) -> pd.DataFrame:
    column_names = [ f'column_{i+1}' for i, val in enumerate(nums[0])]
    df = pd.DataFrame(nums)
    df.columns = column_names
    return df

def file2df_primary(file) -> tuple(list[pd.DataFrame]):
    lines = grab_lines(file)
    data = grab_nums(lines)
    df = nums2df(data)
    
    return df

def file2df(file):
    try:
        df = file2df_primary(file)
        return df
    except Exception:
        try:
            df = pd.read_csv(file, delimiter=det_delim_ex(file), names=['wavelength', 'intensity'])
            return df
        except Exception as e:
            print(f"Error processing file: {file}")
            print(f"Error message: {str(e)}")

def determine_delimiter(file_content):
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
