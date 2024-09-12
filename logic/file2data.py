import pandas as pd
import csv
import io

def file2df(file):
    try:
        lines = grab_lines(file)
        print(lines, 'lines')
        data = grab_nums(lines)
        df = nums2df(data)
        return df
    except Exception:
        try:
            df = pd.read_csv(file, delimiter=det_delim(file), names=['wavelength', 'intensity'])
            return df
        except Exception as e:
            print(f"Error processing file in file2df: {file}")
            print(f"Error message in file2df: {str(e)}")

def grab_lines(file) -> list:
    file.seek(0)    
    lines = [line.decode() for line in file.readlines()]
    return lines

def grab_nums(lines: list) -> list[float]:
    '''
    Takes a list of lines, and tests items in each line that are convertable to a float, 
    
    if any item in line is not convertable, the line is discarded.
    
    '''
    nums = []  # list to hold numbers from the text file
    for line in lines:
        delimiter = determine_delimiter(line)
        split_line = line.split(delimiter)  # remove white space from each line and split into a list
        if split_line and all(is_float(element) for element in split_line):
            nums.append([float(element) for element in split_line])
    return nums


# # UPDATED GRAB NUMS
# def grab_nums(lines: list):
#     nums = []
#     for line in lines:
#         split_line = line.split()
#         if split_line and all(is_float(element) for element in split_line):
#             nums.append([float(element) for element in split_line])
#     return nums

def nums2df(nums: list[float]) -> pd.DataFrame:
    column_names = [ f'column_{i+1}' for i, val in enumerate(nums[0])]
    df = pd.DataFrame(nums)
    df.columns = column_names
    return df

def determine_delimiter(line):
    if '\t' in line:
        return '\t'  # Tab delimiter
    elif ',' in line:
        return ','  # Comma delimiter
    elif ';' in line:
        return ';'  # Semicolon delimiter
    elif ' ' in line:
        return ' '  # Space delimiter (default)
    else:
        print('Could not determine delimiter. Attempted tab, comma, semicolon, and space.')
        return None

def det_delim(file_content):
    with open(file_content, 'r') as file:
        first_line = file.readline()
    return determine_delimiter(first_line)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
