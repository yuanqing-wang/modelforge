import os
from typing import List

import h5py
import requests
import torch
from tqdm import tqdm

from modelforge.utils import HAR2EV, KCALMOL2EV

from .dataset import Dataset


class QM9Dataset(Dataset):
    """
    A specific dataset, extending the abstract Dataset class.
    """

    @property
    def url(self):
        return "https://data.pyg.org/datasets/qm9_v3.zip"

    @property
    def raw_file_path(self):
        return os.path.join(self.cache_dir, "qm9_raw.zip")

    @property
    def processed_file_path(self):
        return os.path.join(self.cache_dir, "qm9_v3.pt")

    @property
    def raw_file_names(self) -> List[str]:
        return ["gdb9.sdf", "gdb9.sdf.csv", "uncharacterized.txt"]

    def prepare_data(self) -> None:
        r"""
        Transform the data from a sdf file to a pytorch pt file format.
        """
        conversion = conversion = torch.tensor(
            [
                1.0,
                1.0,
                HAR2EV,
                HAR2EV,
                HAR2EV,
                1.0,
                HAR2EV,
                HAR2EV,
                HAR2EV,
                HAR2EV,
                HAR2EV,
                1.0,
                KCALMOL2EV,
                KCALMOL2EV,
                KCALMOL2EV,
                KCALMOL2EV,
                1.0,
                1.0,
                1.0,
            ]
        )

        with open(f"{self.extracted_file_path}/{self.raw_file_names[1]}", "r") as f:
            target = f.read().split("\n")[1:-1]
            target = [[float(x) for x in line.split(",")[1:20]] for line in target]
            target = torch.tensor(target, dtype=torch.float)
            target = torch.cat([target[:, 3:], target[:, :3]], dim=-1)
            target = target * conversion.view(1, -1)
        print(target[:10])

    def load(self):
        with open(self.processed_file_path, "r") as fp:
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
