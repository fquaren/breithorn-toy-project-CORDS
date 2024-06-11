import git
import os
import requests
import zipfile
import pandas as pd
import rasterio

def make_sha_filename(basename, ext):
    """
    Generate a filename with a postfix based on the current Git commit.

    The postfix is a 10-character short hash of the current commit ID. If there are
    uncommitted changes in the repository, the postfix will be suffixed with '-dirty'.

    Args:
        basename (str): The base filename without extension.
        ext (str): The file extension.

    Returns:
        str: The filename with the postfix (short hash or short hash with '-dirty').

    """


    # Open the git repository in the current directory
    repo = git.Repo(".")

    # Get the object ID of the HEAD commit
    head_commit_id = repo.head.commit.hexsha
    # Take the first 10 characters of the commit ID
    short_hash = head_commit_id[:10]

    # Check if there are uncommitted changes
    if repo.is_dirty():
        postfix = f"{short_hash}-dirty"
    else:
        postfix = short_hash

    return f"{basename}-{postfix}{ext}"


def download_file(url, destination_file):
    """
    Downloads a file from the given URL to the specified destination.

    If the file already exists at the destination, the function does nothing.
    Otherwise, it downloads the file and saves it to the destination.

    Args:
        url (str): The URL of the file to download.
        destination_file (str): The path where the downloaded file should be saved.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the download.
    """
    # make sure the directory exists
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)

    if os.path.isfile(destination_file):
        # do nothing
        print(f"Already downloaded {destination_file}")
    else:
        # download
        print(f"Downloading {destination_file} ... ", end="")
        response = requests.get(url)
        with open(destination_file, 'wb') as file:
            file.write(response.content)
        print("done.")


def unzip_all_files(zipfile_path, destination_dir):
    """
    Extracts all files from a zip archive to a specified destination directory.

    Args:
        zipfile_path (str): The path to the zip file.
        destination_dir (str): The directory where the extracted files should be saved.

    Raises:
        zipfile.BadZipFile: If the file is not a zip file or it is corrupted.
    """
    # make sure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
        print(f"Extracted all files to {destination_dir}")


# Helper function to save figures with a standardized filename
def make_sha_filename(filepath, extension):
    return f"{filepath}{extension}"


# Read data
def read_campbell(weather_file):
    # Dummy implementation to read weather data
    data = pd.read_csv(weather_file)
    t = data['time'].values
    Ts = data['temperature'].values
    return t, Ts


def read_ascii_grid(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
    return data