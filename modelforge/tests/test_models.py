from typing import Optional

import pytest
import torch

from modelforge.potential.models import BaseNNP
from modelforge.potential.schnet import Schnet
from .helper_functinos import default_input

MODELS_TO_TEST = [Schnet]


def setup_simple_model(model_class) -> Optional[BaseNNP]:
    if model_class is Schnet:
        return Schnet(n_atom_basis=128, n_interactions=3, n_filters=64)
    else:
        raise NotImplementedError


def test_BaseNNP():
    nnp = BaseNNP(dtype=torch.float32, device="cpu")
    assert nnp.dtype == torch.float32
    assert str(nnp.device) == "cpu"


@pytest.mark.parametrize("model_class", MODELS_TO_TEST)
def test_forward_pass(model_class):
    initialized_model = setup_simple_model(model_class)
    inputs = default_input()
    output = initialized_model.forward(inputs)