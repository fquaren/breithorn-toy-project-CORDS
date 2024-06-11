import sys
sys.path.insert(1, 'src')
import os

from utils import *


# Setup project folder
os.makedirs('data/own', exist_ok=True)
os.makedirs('data/foreign', exist_ok=True)

# Download data

# weather
download_file("https://raw.githubusercontent.com/mauro3/CORDS/master/data/workshop-reproducible-research/own/weather.dat", "data/own/weather.dat")

# glacier mask
download_file("https://github.com/mauro3/CORDS/raw/master/data/workshop-reproducible-research/own/mask_breithorngletscher.zip", "data/own/mask.zip")
unzip_all_files("data/own/mask.zip", "data/own/mask")

# digital elevation model (DEM)
download_file("https://github.com/mauro3/CORDS/raw/master/data/workshop-reproducible-research/foreign/swisstopo_dhm200_cropped.zip", "data/foreign/DEM.zip")
unzip_all_files("data/foreign/DEM.zip", "data/foreign/DEM")

