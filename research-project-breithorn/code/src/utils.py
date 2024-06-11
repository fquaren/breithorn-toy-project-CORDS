import git

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
