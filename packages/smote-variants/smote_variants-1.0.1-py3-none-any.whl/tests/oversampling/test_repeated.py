"""
Tests oversamplers with repeated samples
"""

import logging

import pytest
import numpy as np

import smote_variants as sv

from smote_variants.datasets import load_repeated

# disabling smote-variants logging

logger = logging.getLogger("smote_variants")
logger.setLevel(logging.CRITICAL)

dataset = load_repeated()


@pytest.mark.parametrize("smote_class", sv.get_all_oversamplers())
def test_repeated(smote_class):
    """
    Tests oversamplers with repeated samples

    Args:
        smote_class (class): an oversampling class
    """
    X, y = smote_class().sample(dataset["data"], dataset["target"])

    assert np.unique(y).shape[0] == 2
    assert X.shape[0] > 0
