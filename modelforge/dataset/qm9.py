from .dataset import Dataset
from tqdm import tqdm
import os
import requests
import h5py


class QM9Dataset(Dataset):
    """
    A specific dataset, extending the abstract Dataset class.
    """

    @property
    def cache_path(self):
        return os.path.join(self.cache_dir, "qm9.hdf5")

    def download(self):
        if not os.path.exists(self.cache_path):
            # Download the file
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Raise an HTTPError if the response contains an HTTP status code

            file_size = int(response.headers.get("Content-Length", 0))
            progress = tqdm(
                response.iter_content(1024),
                f"Downloading {self.url}",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            )

            # Save the file
            with open(self.cache_path, "wb") as fp:
                for chunk in progress.iterable:
                    if chunk:
                        fp.write(chunk)
                    # update the progress bar manually
                    progress.update(len(chunk))

    def load(self):
        with open(self.cache_path, "r") as fp:
            data = fp.read()  # This would depend on your file format
        return data

    def preprocess(self, data):
        # Preprocess your data here
        processed_data = data
        return processed_data

    def query(self, **kwargs):
        # Query your data here
        result = None
        return result
