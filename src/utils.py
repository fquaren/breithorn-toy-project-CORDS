import git

def make_sha_filename(basename, ext):
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
