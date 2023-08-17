import os
from typing import Any, Dict, List, Tuple

import gdown
import h5py
import numpy as np
import torch
from loguru import logger
from .dataset import BaseDataset


class QM9Dataset(BaseDataset):
    """
    Dataset class for handling QM9 data.

    Provides utilities for processing and interacting with QM9 data stored in hdf5 format.
    Also allows for lazy loading of data or caching in memory for faster operations.
    """

    def __init__(
        self,
        dataset_name: str = "QM9",
        load_in_memory: bool = True,
        test_data: bool = False,
    ) -> None:
        """
        Initialize the QM9Dataset class.

        Parameters:
        -----------
        dataset_name : str
            Name of the dataset, default is "QM9".
        load_in_memory : bool
            Flag to determine if the dataset should be loaded into memory, default is True.
        test_data : bool
            If set to true it will only load a small fraction of the QM9 dataset.
        """

        if test_data:
            dataset_name = f"{dataset_name}_subset"
        self.dataset_name = dataset_name
        self.keywords_for_hdf5_dataset = ["geometry", "atomic_numbers", "return_energy"]
        self.test_data = test_data
        self._dataset = None  # private _dataset attribute
        super().__init__()

    def load_or_process_data(self) -> None:
        """
        Loads the dataset from cache if available, otherwise processes and caches the data.
        """

        if not os.path.exists(self.processed_dataset_file):
            if not os.path.exists(self.raw_dataset_file):
                self.download_hdf_file()
            data = self.from_hdf5()
            self.to_file_cache(data)

        self.from_file_cache()

    def to_npz(self, data: Dict[str, Any]) -> None:
        """
        Save processed data to a numpy (.npz) file.

        Parameters:
        -----------
        data : Dict[str, Any]
            Dictionary containing processed data to be saved.
        """
        max_len_species = max(len(arr) for arr in data["atomic_numbers"])

        padded_coordinates = BaseDataset.pad_molecules(data["geometry"])
        padded_atomic_numbers = BaseDataset.pad_to_max_length(
            data["atomic_numbers"], max_len_species
        )
        logger.debug(f"Writing data cache to {self.processed_dataset_file}")

        np.savez(
            self.processed_dataset_file,
            coordinates=padded_coordinates,
            atomic_numbers=padded_atomic_numbers,
            return_energy=np.array(data["return_energy"]),
        )

    def _download_from_gdrive(self):
        """Internal method to download the dataset from Google Drive."""

        test_id = "13ott0kVaCGnlv858q1WQdOwOpL7IX5Q9"
        full_id = "1_bSdQjEvI67Tk_LKYbW0j8nmggnb5MoU"
        if self.test_data:
            logger.debug("Downloading test data")
            id = test_id
        else:
            logger.debug("Downloading full dataset")

            id = full_id
        url = f"https://drive.google.com/uc?id={id}"
        gdown.download(url, self.raw_dataset_file, quiet=False)

        if self.is_gzipped(self.raw_dataset_file):
            logger.debug("Decompressing gzipped file")
            os.rename(f"{self.raw_dataset_file}", f"{self.raw_dataset_file}.gz")
            self.decompress_gziped_file(
                f"{self.raw_dataset_file}.gz", self.raw_dataset_file
            )

    def download_hdf_file(self):
        """
        Download the hdf5 file containing the dataset.

        Fetches the dataset from the specified source (Google Drive in this case)
        and saves it in hdf5 format.
        """
        self._download_from_gdrive()

    def __len__(self) -> int:
        """
        Return the number of datapoints in the dataset.

        Returns:
        --------
        int
            Total number of datapoints available in the dataset.
        """
        return len(self.dataset["atomic_numbers"])

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Fetch a tuple of geometry, atomic numbers, and energy for a given molecule index.

        Parameters:
        -----------
        idx : int
            Index of the molecule to fetch data for.

        Returns:
        --------
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor]
            Tuple containing tensors for geometry, atomic numbers, and energy of the molecule.
        """
        return (
            torch.tensor(self.dataset["coordinates"][idx]),
            torch.tensor(self.dataset["atomic_numbers"][idx]),
            torch.tensor(self.dataset["return_energy"][idx]),
        )

    @property
    def dataset(self) -> Dict[str, np.ndarray]:
        """Getter for dataset. Loads the dataset if not already loaded."""
        if self._dataset is None:
            self.load_or_process_data()

        return self._dataset

    @dataset.setter
    def dataset(self, value: Dict[str, np.ndarray]):
        """Setter for dataset. Sets the dataset value."""
        self._dataset = value