import sys
sys.path.insert(1, 'src')
import os

from utils import *


# Uncomment to test download funtion
# download_file('https://upload.wikimedia.org/wikipedia/commons/9/9b/Breithorn.jpg', './Breithorn.jpg')


# This script prepares data for Breithorngletscher near Zermatt, Switzerland

## Setup project folder
os.makedirs('data/own', exist_ok=True)
os.makedirs('data/foreing', exist_ok=True)

## Download data
# weather
download_file("https://github.com/mauro3/CORDS/blob/master/data/workshop-reproducible-research/own/weather.dat", "data/own/weather.dat")

# glacier mask
download_file("https://doi.glamos.ch/data/inventory/inventory_sgi2016_r2020.zip", "data/own/mask.zip")
unzip_all_files("data/own/mask.zip", "data/own/mask")

# digital elevation model (DEM)
download_file("https://data.geo.admin.ch/ch.swisstopo.digitales-hoehenmodell_25/data.zip", "data/foreign/DEM.zip")
unzip_all_files("data/foreign/DEM.zip", "data/foreign/DEM")


## Some extra data, manually entered
z_weather_station = 2650 # elevation of weather station [m]
Ps0 = 0.005 # mean (and constant) precipitation rate [m/d]
