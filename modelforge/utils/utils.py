import zipfile


def extract_zip(path: str, folder: str):
    r"""Extracts a zip archive to a specific folder.

    Args:
        path (str): The path to the tar archive.
        folder (str): The folder.
    """

    with zipfile.ZipFile(path, "r") as f:
        f.extractall(folder)
