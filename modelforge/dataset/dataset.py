import os
from abc import ABC, abstractmethod
from typing import List

import requests
import torch
from tqdm import tqdm

from modelforge.utils import extract_zip, HAR2EV, KCALMOL2EV


"""
The Dataset class defines the interface for datasets as a ABC.
Each specific dataset has to implement the following methods:
- raw_file_path (the path where the raw dataset should be stored)
- processed_file_path (the path where the extracted and processed dataset should be stored)
- prepare_data (the method that transforms the raw dataset to the processed dataset)
    * the processed data will be saved as a pytorch pt file
- load (the method that loads the dataset from the cache)



NOTE: How should we best cache data?
NOTE: What is the most appropriate internal data format?

"""


class Dataset(torch.utils.data.Dataset, ABC):
    """
    Abstract Base Class representing a dataset.
    """

    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir

    @property
    def name(self) -> str:
        """
        Returns the name of the dataset.

        Returns:
            str: name of the dataset
        """
        return self.__class__.__name__

    @property
    @abstractmethod
    def raw_file_path(self) -> str:
        """
        Returns the path where the raw dataset should be stored.

        Returns:
            str: file path to the raw dataset
        """
        pass

    @property
    @abstractmethod
    def processed_file_path(self) -> str:
        """
        Returns the path were the

        Returns:
            str: _description_
        """
        pass

    def _download_raw(self) -> None:
        """
        Downloads the raw dataset.
        """
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
        with open(self.raw_file_path, "wb") as fp:
            for chunk in progress.iterable:
                if chunk:
                    fp.write(chunk)
                # update the progress bar manually
                progress.update(len(chunk))

    @property
    @abstractmethod
    def raw_file_names(self) -> List[str]:
        pass

    @abstractmethod
    def prepare_data(self):
        pass

    @property
    def extracted_file_path(self) -> str:
        return f"{self.cache_dir}/{self.name}_extracted/"

    def download(self) -> None:
        if not os.path.exists(self.processed_file_path):
            if not os.path.exists(self.raw_file_path):
                self._download_raw()
            extract_zip(self.raw_file_path, f"{self.extracted_file_path}")
            # Download the file
        else:
            print(f"Using cached file {self.processed_file_path}")

        self.prepare_data()

    @abstractmethod
    def load(self):
        """
        Loads the dataset from the cache.
        """
        pass

    # @abstractmethod
    # def query(self, **kwargs):
    #     """
    #     Queries the dataset.
    #     """
    #     pass
