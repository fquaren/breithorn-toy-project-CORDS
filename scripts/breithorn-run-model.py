import pandas as pd
import pdb
import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

import sys
sys.path.insert(1, 'src')
from utils import *
from melt import *


# Some extra data, manually entered
z_weather_station = 2650 # elevation of weather station [m]
Ps0 = 0.005 # mean (and constant) precipitation rate [m/d]


# Read data
def read_weather_data(weather_file):
    columns = ["111", "year", "day", "hour", "rel. humidity", "air temp.", "perciptation [mm / 30min]", "batt. voltage", "internal temp"]
    ds = pd.read_csv(weather_file, names=columns)
    t = ds["year"].to_numpy()
    Ts = ds["air temp."].to_numpy()
    return t, Ts


import numpy as np
import pandas as pd
from datetime import datetime, timedelta

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

# Test the function
assert parse_campbell_date_time(2007, 1, 1239) == datetime(2007, 1, 1, 12, 39)
assert parse_campbell_date_time(2007, 365, 2359) == datetime(2007, 12, 31, 23, 59)

# Example usage
file_path = 'path/to/your/campbell_file.csv'




def read_ascii_grid(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
    return data



def read_and_visualize_ascii_grid(file_path):
    """
    Reads and visualizes an ASCII grid file.

    Args:
        file_path (str): The path to the ASCII grid file.
    """
    try:
        with rasterio.open(file_path) as src:
            data = src.read(1)  # Read the first band
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            show(data, ax=ax, cmap='viridis')
            ax.set_title(f'Visualization of {file_path}')
            plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
            plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")



def heatmap(data, title, output_file):
    """
    Creates a heatmap of the given data.

    Args:
        data (array): The data to be plotted.
        title (str): The title of the heatmap.
        output_file (str): The file to save the heatmap.
    """
    plt.imshow(data, cmap='viridis')
    plt.colorbar()
    plt.title(title)
    plt.savefig(output_file)
    plt.show()


file_path_dem = "/home/fquaren/work/breithorn-toy-project-CORDS/data/foreign/DEM/swisstopo_dhm200_cropped/dhm200_cropped.asc"
file_path_mask = "/home/fquaren/work/breithorn-toy-project-CORDS/data/own/mask/mask_breithorngletscher/mask_breithorngletscher.asc"
dem = np.array(read_ascii_grid(file_path_dem))
mask = np.array(read_ascii_grid(file_path_mask))
# t, Ts = read_weather_data("data/own/weather.dat")
t, Ts = read_campbell("data/own/weather.dat")
Ps = Ps0*np.ones(len(Ts))
lapse_rate = -0.6/100
melt_factor = 0.005
T_threshold = 4
results_dir = 'results'

# Run the model for the whole Breithorn glacier
zs = dem[mask == 1] - z_weather_station  # Select glacier points and use elevation of weather station as datum
dt = float((t[1].hour - t[0].hour))/24
total_massbalance, point_massbalance = glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)

# Make a map again
point_massbalance_map = np.full_like(dem, np.nan)  # Create a map filled with NaNs
point_massbalance_map[mask == 1] = point_massbalance

# Save the mass balance map
output_file = make_sha_filename(os.path.join(results_dir, "breithorn_massbalance_field"), ".png")
print(output_file)
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