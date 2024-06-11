import git
import os
import requests
import zipfile

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

# Example usage
# download_file('https://example.com/file.txt', 'path/to/destination/file.txt')


def unzip_one_file(zipfile_path, filename, destination_file):
    """
    Extracts a specific file from a zip archive to a specified destination.

    Args:
        zipfile_path (str): The path to the zip file.
        filename (str): The name of the file to extract from the zip archive.
        destination_file (str): The path where the extracted file should be saved.

    Raises:
        FileNotFoundError: If the specified file is not found in the zip archive.
    """
    # make sure the directory exists
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)

    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        try:
            with zip_ref.open(filename) as source_file:
                with open(destination_file, 'wb') as dest_file:
                    dest_file.write(source_file.read())
            print(f"Extracted {filename} to {destination_file}")
        except KeyError:
            raise FileNotFoundError(f"{filename} not found in the zip archive.")

# Example usage
# unzip_one_file('path/to/zipfile.zip', 'file_to_extract.txt', 'path/to/destination/file.txt')
