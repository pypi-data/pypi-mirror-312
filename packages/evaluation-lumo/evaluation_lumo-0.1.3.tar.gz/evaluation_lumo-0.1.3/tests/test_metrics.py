import pytest
from evaluation_lumo.metrics import compute_tr, mean_ratio
import numpy as np
import pandas as pd
TEST_CASES = [
    # Scenario 1: Balanced case
    ([0.1, 0.3, 0.5, 0.7, 0.9], 0.5, 2/5),

    # Scenario 2: No true positives (all scores below threshold)
    ([0.1, 0.2, 0.3, 0.4], 0.5, 0.0),

    # Scenario 3: All true positives (all scores above threshold)
    ([0.6, 0.7, 0.8, 0.9], 0.5, 1.0),
]

@pytest.mark.parametrize("damage_indexs, threshold, expected_tpr", TEST_CASES)
def test_compute_tr(damage_indexs, threshold, expected_tpr):
    tpr = compute_tr(damage_indexs, threshold)
    assert tpr == pytest.approx(expected_tpr, rel=1e-6)


# Define test cases for the mean_ratio function
test_cases = [
    # Scenario 1: Normal case with numpy arrays (no warning expected)
    {"healthy_scores": np.array([1.0, 2.0, 3.0]), "damaged_scores": np.array([3.0, 4.0, 5.0]), "expected_ratio": 1, "warns": False},
    
    # Scenario 2: Healthy and damaged as Pandas Series (no warning expected)
    {"healthy_scores": pd.Series([1.0, 2.0, 3.0]), "damaged_scores": pd.Series([3.0, 4.0, 5.0]), "expected_ratio": 1, "warns": False},
    
    # Scenario 3: List input (no warning expected)
    {"healthy_scores": [1.0, 2.0, 3.0], "damaged_scores": [6.0, 6.0, 6.0], "expected_ratio": 3/2, "warns": False},
    
    # Scenario 4: Edge case with identical healthy and damaged scores (warning expected)
    {"healthy_scores": [2.0, 2.0, 2.0], "damaged_scores": [2.0, 2.0, 2.0], "expected_ratio": 1, "warns": True},
    
    # Scenario 5: Single value in healthy and damaged (warning expected)
    {"healthy_scores": [1.0], "damaged_scores": [2.0], "expected_ratio": 2.0, "warns": True},
]

@pytest.mark.parametrize("case", test_cases)
def test_mean_ratio(case):
    """
    Test the mean_ratio function with various inputs, checking for warnings when appropriate.
    """
    # Extract test case data
    healthy_scores = case["healthy_scores"]
    damaged_scores = case["damaged_scores"]
    expected_ratio = case["expected_ratio"]
    expects_warning = case["warns"]

    # Test for warnings when applicable
    if expects_warning:
        with pytest.warns(UserWarning) as record:
            ratio = mean_ratio(damage_index_healthy=healthy_scores, damage_index_damaged=damaged_scores)
            assert np.isclose(ratio, expected_ratio)
            assert expects_warning == (len(record) == 1)
    else:
        ratio = mean_ratio(damage_index_healthy=healthy_scores, damage_index_damaged=damaged_scores)
        assert np.isclose(ratio, expected_ratio)
