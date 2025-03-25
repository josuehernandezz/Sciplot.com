import numpy as np
from scipy.interpolate import pchip_interpolate
from .file2data import file2df

def correction_maker(manufacturer_file, measurement_file):
    # Extract data from files
    # Lamp spectral response
    manufacturer_data = file2df(manufacturer_file)
    # Raw calibration Data
    measurement_data = file2df(measurement_file)

    # Get x and y columns and store them in their respective variables
    manufacturer_x = manufacturer_data.iloc[:, 0]
    manufacturer_y = manufacturer_data.iloc[:, 1]

    # Get x and y columns and store them in their respective variables
    measurement_x = measurement_data.iloc[:, 0]
    measurement_y = measurement_data.iloc[:, 1]

    # Interpolate new data points in between the original
    manufacturer_y_interp = pchip_interpolate(manufacturer_x, manufacturer_y, measurement_x)

    correction_y = measurement_y / manufacturer_y_interp

    return np.column_stack((measurement_x, correction_y))
