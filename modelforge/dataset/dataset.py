from abc import ABC, abstractmethod


class Dataset(ABC):
    """
    Abstract Base Class representing a dataset.
    """

    def __init__(self, url, cache_dir):
        self.url = url
        self.cache_dir = cache_dir

    @property
    @abstractmethod
    def cache_path(self):
        """
        Returns the path where the dataset should be cached.
        """
        pass

    @abstractmethod
    def download(self):
        """
        Downloads the dataset.
        """
        pass

    @abstractmethod
    def load(self):
        """
        Loads the dataset from the cache.
        """
        pass

    @abstractmethod
    def preprocess(self, data):
        """
        Preprocesses the dataset.
        """
        pass

    @abstractmethod
    def query(self, **kwargs):
        """
        Queries the dataset.
        """
        pass


