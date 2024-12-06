import pytest
import pandas as pd
from evaluation_lumo.utils import label_events
from evaluation_lumo.config import mat_state

@pytest.fixture
def setup_data():
    # Sample timestamps for testing
    timestamps = pd.date_range(start="2020-08-01", end="2021-08-06", freq="D")

    # Define events as dictionaries
    events = {
        "healthytrain": {
            "start": "2020-08-01",
            "end": "2020-10-27T10:00:00",
            "description": "all damage mechanisms removed"
        },
        "healthytest": {
            "start": "2020-10-27",
            "end": "2020-11-09",
            "description": "healthy state after damage"
        },
        "damage1": {
            "start": "2020-11-09",
            "end": "2020-11-24",
            "description": "all damage mechanisms removed",
            "severity": "high",
            "location": "DAM4",
            "closest_sensor": 6
        }
    }
    return timestamps, events

def test_label_events(setup_data):
    timestamps, events = setup_data

    # Apply the label_events function
    result_labels = label_events(timestamps, events)

    # Check that the result is a pandas Series
    assert isinstance(result_labels, pd.Series)

    # Check that the length of the result matches the input timestamps
    assert len(result_labels) == len(timestamps)

    # Check specific dates to ensure correct labeling
    test_cases = {
        "2020-08-02": "healthytrain",
        "2020-10-28": "healthytest",
        "2020-11-10": "damage1",
        "2021-01-01": 'no_event'  # Assuming 0 indicates no event
    }

    for date_str, expected_label in test_cases.items():
        date = pd.Timestamp(date_str)
        label = result_labels[timestamps == date].values[0]
        assert label == expected_label


def test_label_events():
    timestamps = pd.date_range(start="2020-08-01", end="2022-01-20", freq="10min")
    events = label_events(timestamps, mat_state)
    # count the number of each event 
    res = events.value_counts()
    assert res['healthy_train'] == 8784
    assert res['healthy_test'] == 1728
    assert res['no_event'] == 24768
    assert res['damage1'] == 2016
    assert res['damage2'] == 2160
    assert res['damage3'] == 4752
    assert res['damage4'] == 2160
    assert res['damage5'] == 2448
    assert res['damage6'] == 2448
    assert res['healthy1'] == 1872
    assert res['healthy2'] == 16416
    assert res['healthy3'] == 2016
    assert res['healthy4'] == 1296
    assert res['healthy5'] == 1584
    assert res['healthy6'] == 2881
