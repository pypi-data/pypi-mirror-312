"""
Testing oversampling with 2 minority sample only.
"""

import logging

import pytest
import numpy as np

import smote_variants as sv

from smote_variants.datasets import load_2_min_some_maj
from .additional_objs import additional_objs

# disabling smote-variants logging

logger = logging.getLogger("smote_variants")
logger.setLevel(logging.CRITICAL)

dataset = load_2_min_some_maj()


@pytest.mark.parametrize("smote_class", sv.get_all_oversamplers())
def test_2_min_some_maj(smote_class):
    """
    Testing oversamplers with 2 minority samples.

    Args:
        smote_class (class): an oversampler class.
    """
    X, y = smote_class().sample(dataset["data"], dataset["target"])

    assert np.unique(y).shape[0] == 2
    assert X.shape[0] > 0


@pytest.mark.parametrize("smote_obj", additional_objs)
def test_2_min_some_maj_additional(smote_obj):
    """
    Testing oversamplers with 2 minority samples.

    Args:
        smote_obj (obj): an oversampler obj
    """
    X, y = smote_obj.sample(dataset["data"], dataset["target"])

    assert np.unique(y).shape[0] == 2
    assert X.shape[0] > 0
