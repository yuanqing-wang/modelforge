import sys


def test_dataset_imported():
    """Sample test, will always pass so long as import statement worked."""
    import modelforge.dataset

    assert "modelforge.dataset" in sys.modules


def test_download_qm9_dataset():
    from modelforge.dataset import QM9Dataset

    processed_url = "https://data.pyg.org/datasets/qm9_v3.zip"

    qm9_dataset = QM9Dataset(processed_url, "/tmp").download()
