import pytest
import numpy as np
import pandas as pd
from evaluation_lumo.evaluation import prepare_dataframe, compute_tr_by_events, compute_mean_variation

# Mock `mat_state` configuration
mock_mat_state = {
    "healthy_train": {"start": "2023-01-01", "end": "2023-01-10"},
    "damage_1": {"start": "2023-01-11", "end": "2023-01-15"},
    "healthy_2": {"start": "2023-01-16", "end": "2023-01-20"},
}

@pytest.fixture
def mock_events():
    return mock_mat_state

@pytest.fixture
def mock_data():
    timestamps = pd.date_range(start="2023-01-01", end="2023-01-20", freq="10min")
    damage_indexs = np.random.random(len(timestamps))  # Random anomaly scores
    return timestamps, damage_indexs

@pytest.fixture
def perfect_data():

    # Configuration of time ranges and their anomaly score properties
    time_ranges = [
        {"start": "2023-01-01", "end": "2023-01-10", "low": 0.0, "high": 0.1},  # Healthy training
        {"start": "2023-01-11", "end": "2023-01-15", "low": 10.0, "high": 11.0},  # Damage period
        {"start": "2023-01-16", "end": "2023-01-20", "low": 0.0, "high": 0.1},  # Healthy period
    ]

    # Generate timestamps
    timestamps = pd.date_range(start="2023-01-01", end="2023-01-20", freq="1h")
    scores = pd.Series(index=timestamps, dtype=float)  # Initialize scores as a Series

    # Assign scores based on defined time ranges
    for time_range in time_ranges:
        mask = (timestamps >= time_range["start"]) & (timestamps <= time_range["end"])
        scores[mask] = np.random.uniform(time_range["low"], time_range["high"], mask.sum()
        )

    return timestamps, scores

def test_prepare_dataframe(mock_events, mock_data):
    """
    Test the `prepare_dataframe` function for correctness.
    """
    timestamps, damage_indexs = mock_data
    data, train_data = prepare_dataframe(timestamps, damage_indexs, mock_events)

    # Assert the output types
    assert isinstance(data, pd.DataFrame), "Data should be a pandas DataFrame."
    assert isinstance(train_data, np.ndarray), "Train data should be a array."

    # Assert data content
    assert 'event' in data.columns, "Data should contain 'event' column."
    assert len(data) == len(timestamps), "Data length should match timestamps length."

    # Assert training data
    assert len(train_data) > 0, "Train data should not be empty."
    assert np.allclose(data[data['event'] == 'healthy_train']['score'].values, train_data), \
        "Train data should match healthy training data."

def test_compute_tr_by_events(mock_events, mock_data):
    """
    Test the `compute_tr_by_events` function for correctness.
    """
    timestamps, damage_indexs = mock_data

    # Run the function
    result,tr = compute_tr_by_events(
        timestamps=timestamps,
        damage_indexs=damage_indexs,
        fpr_train=0.01,
        events=mock_events
    )
    # Assert the output type
    assert isinstance(result, dict), "Result should be a dictionary."

    # Assert keys in the result correspond to events
    expected_events = set(mock_events.keys())
    assert expected_events.issubset(result.keys()), "Result keys should match the events."

    # Assert all values are floats
    assert all(isinstance(v, float) for v in result.values()), "All values in the result should be floats."

def test_compute_mean_variation(mock_events, mock_data):
    """
    Test the `compute_mean_variation` function for correctness.
    """
    timestamps, damage_indexs = mock_data

    # Run the function
    result = compute_mean_variation(
        timestamps=timestamps,
        damage_indexs=damage_indexs,
        events=mock_events
    )

    # Assert the output type
    assert isinstance(result, dict), "Result should be a dictionary."

    # Assert keys in the result correspond to events
    expected_events = set(mock_events.keys())
    assert expected_events.issubset(result.keys()), "Result keys should match the events."

    # Assert all values are floats
    assert all(isinstance(v, float) for v in result.values()), "All values in the result should be floats."



def test_compute_tr_by_events_perfect_detector(mock_events, perfect_data):
    """
    Test `compute_tr_by_events` function with a perfect detector scenario.
    """
    timestamps, damage_indexs = perfect_data

    # Run the function
    result,tr = compute_tr_by_events(
        timestamps=timestamps,
        damage_indexs=damage_indexs,
        fpr_train=0.01,
        events=mock_events
    )

    # True Positive Rate (TPR) should be 1.0 for `damage_1` and 0.0 for healthy events
    assert result['damage_1'] == pytest.approx(1.0, rel=1e-6), "TPR for damage_1 should be 1.0."
    assert result['healthy_train'] == pytest.approx(0.02, abs=0.01), "TPR for healthy_train should be 0.01"
    assert tr == pytest.approx(0.1, rel=5e-2), "Threshold should be 0.1."

def test_compute_mean_variation_perfect_detector(mock_events, perfect_data):
    """
    Test `compute_mean_variation` function with a perfect detector scenario.
    """
    timestamps, damage_indexs = perfect_data

    # Run the function
    result = compute_mean_variation(
        timestamps=timestamps,
        damage_indexs=damage_indexs,
        events=mock_events
    )

    # Mean variation should reflect the contrast between damage and healthy scores
    assert result['damage_1'] > result['healthy_train'], "Mean variation for damage_1 should be higher than healthy_train."
    assert result['damage_1'] > result['healthy_2'], "Mean variation for damage_1 should be higher than healthy_2."