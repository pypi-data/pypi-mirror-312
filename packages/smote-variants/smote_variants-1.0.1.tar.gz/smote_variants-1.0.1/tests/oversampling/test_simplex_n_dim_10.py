"""
Testing oversampling with simplex sampling dim 10.
"""

import logging

import pytest
import numpy as np

import smote_variants as sv

from smote_variants.datasets import load_illustration_2_class

# disabling smote-variants logging

logger = logging.getLogger("smote_variants")
logger.setLevel(logging.CRITICAL)

dataset = load_illustration_2_class()


@pytest.mark.parametrize(
    "smote_class",
    sv.get_simplex_sampling_oversamplers(
        exclude_within_simplex_sampling="deterministic"
    ),
)
def test_simplex_dim_10(smote_class):
    """
    Testing oversamplers with simplex sampling dim 10.

    Args:
        smote_class (class): an oversampler class.
    """
    ss_params = {"n_dim": 10}
    X, y = smote_class(ss_params=ss_params).sample(dataset["data"], dataset["target"])

    assert np.unique(y).shape[0] == 2
    assert X.shape[0] > 0
