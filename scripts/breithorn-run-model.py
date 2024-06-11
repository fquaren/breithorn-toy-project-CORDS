import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import sys
sys.path.insert(1, 'src')
from utils import *
from melt import *
from params import *


# Read weather data
def read_campbell(file):
    """
    Reads a Campbell logger format file with temperature (ignores other data).

    Args:
        file (str): Path to the Campbell logger format file.

    Returns:
        tuple: (t, temp)
            - t (np.ndarray): Array of DateTime objects.
            - temp (np.ndarray): Array of temperatures in Celsius.
    """
    # Read data
    dat = pd.read_csv(file, header=None)
    
    y, d, hm = dat.iloc[:, 1], dat.iloc[:, 2], dat.iloc[:, 3]
    t = np.array([parse_campbell_date_time(year, day, hhmm) for year, day, hhmm in zip(y, d, hm)])
    
    # Go from 30min intervals to 60min intervals
    t = t[::2]
    temp = dat.iloc[::2, 5].values
    
    return t, temp


def parse_campbell_date_time(year, day, HHMM):
    """
    Parses the Campbell logger time format: `year, day of year, HHMM`.

    Args:
        year (int): Year.
        day (int): Day of the year.
        HHMM (int): Time in HHMM format.

    Returns:
        datetime: DateTime object representing the parsed date and time.
    """
    assert year == 2007, "Year must be 2007"
    
    hour = HHMM // 100
    minute = HHMM % 100
    date = datetime(year, 1, 1) + timedelta(days=day-1, hours=hour, minutes=minute)
    
    return date


def read_ascii_grid(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
    return data


def heatmap(data, title, output_file):
    """
    Creates a heatmap of the given data.

    Args:
        data (array): The data to be plotted.
        title (str): The title of the heatmap.
        output_file (str): The file to save the heatmap.
    """
    plt.imshow(data, cmap='viridis')
    plt.colorbar(label="Point mass balance [m/d]")
    plt.title(title)
    plt.savefig(output_file)
    plt.show()


file_path_dem = "data/foreign/DEM/swisstopo_dhm200_cropped/dhm200_cropped.asc"
file_path_mask = "data/own/mask/mask_breithorngletscher/mask_breithorngletscher.asc"
file_path_weather = "data/own/weather.dat"
results_dir = 'results'

dem = np.array(read_ascii_grid(file_path_dem))
mask = np.array(read_ascii_grid(file_path_mask))
t, Ts = read_campbell(file_path_weather)
Ps = Ps0*np.ones(len(Ts))
lapse_rate = -0.6/100
melt_factor = 0.005
T_threshold = 4

# Run the model for the whole Breithorn glacier
zs = dem[mask == 1] - z_weather_station  # Select glacier points and use elevation of weather station as datum
dt = float((t[1].hour - t[0].hour))/24
total_massbalance, point_massbalance = glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)

# Make a map again
point_massbalance_map = np.full_like(dem, np.nan)  # Create a map filled with NaNs
point_massbalance_map[mask == 1] = point_massbalance

# Save the mass balance map
output_file = make_sha_filename(os.path.join(results_dir, "breithorn_massbalance_field"), ".png")

heatmap(point_massbalance_map, "Point Mass Balance Map", output_file)

# Generate output table
# Make a table for mass balance of different temperature offsets and store it
out = []

for dT in range(-4, 5):
    Ts_ = Ts + dT
    massbalance_, _ = glacier_net_balance_fn(zs, dt, Ts_, Ps, melt_factor, T_threshold, lapse_rate)
    out.append([dT, massbalance_])

output_table = pd.DataFrame(out, columns=["dT", "massbalance"])
output_table_file = make_sha_filename(os.path.join(results_dir, "deltaT_impact"), ".csv")
output_table.to_csv(output_table_file, index=False)