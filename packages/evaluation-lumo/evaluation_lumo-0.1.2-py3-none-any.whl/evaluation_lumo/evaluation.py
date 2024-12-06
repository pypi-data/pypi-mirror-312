import numpy as np
import pandas as pd
from evaluation_lumo.config import mat_state
from evaluation_lumo.utils import label_events
from evaluation_lumo.metrics import compute_tr, mean_ratio
from functools import partial
from typing import Union

def prepare_dataframe(timestamps: Union[pd.Series, np.ndarray],
                      anomaly_scores: Union[pd.Series, np.ndarray],
                      events: dict | None = None,
                      train_start: str | None = None,
                      train_end: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Prepare a pandas DataFrame with labeled events and split into training and full dataframes.
    
    Parameters:
    ----------
    timestamps : pd.Series | np.array
        Array or series of timestamps.
    anomaly_scores : pd.Series | np.array
        Array or series of anomaly scores.
    events : dict | None, optional
        Dictionary with event details. Default is None. If not provided, `mat_state` from the `config` module will be used.
    train_start : str | None, optional
        Start timestamp for the training window. Default is None.
    train_end : str | None, optional
        End timestamp for the training window. Default is None.
    
    Returns:
    -------
    tuple[pd.DataFrame, pd.DataFrame, dict]
        - `data`: Full dataframe with labeled events.
        - `train_data`: Dataframe with training data based on the training window.
        - `events`: Updated event dictionary if not provided.
    """
    # Use mat_state if events is not provided
    if events is None:
        events = mat_state
    if train_start is None or train_end is None:
        train_start = events["healthy_train"]['start']
        train_end = events["healthy_train"]['end']

    
    # Create the dataframe and label events

    data = pd.DataFrame({'timestamp': timestamps, 'score': anomaly_scores})
    events_list = label_events(data['timestamp'].values, events)
    data.loc[:, 'event'] = events_list.values
    train_data = data[(timestamps >= train_start) & (timestamps <= train_end)]['score'].values

    return data, train_data

def compute_tr_by_events(timestamps: Union[pd.Series, np.ndarray],
                         anomaly_scores: Union[pd.Series, np.ndarray],
                         fpr_train: float = 0.01,
                         events: dict | None = None,
                         train_start: str | None = None,
                         train_end: str | None = None) -> dict:
    """
    Compute the True Rate (TR) for each event in the events dictionary. 
    The threshold is set to ensure the False Positive Rate (FPR) is 0.01 for healthy training data.
    """
    # Prepare the data
    data, train_data = prepare_dataframe(timestamps, anomaly_scores, events, train_start, train_end)

    # Compute the threshold based on the training data
    threshold = np.quantile(train_data, 1 - fpr_train)
    # Compute True Rate for each event
    res = data.groupby('event').apply(lambda x: compute_tr(x['score'], threshold),include_groups=False)
    return res.to_dict(), threshold


def compute_mean_variation(timestamps: Union[pd.Series, np.ndarray],
                           anomaly_scores: Union[pd.Series, np.ndarray],
                           events: dict | None = None,
                           train_start: str | None = None,
                           train_end: str | None = None) -> float:
    """
    Compute the mean variation of anomaly scores for each event in the events dictionary.
    """
    # Prepare the data
    data, train_data = prepare_dataframe(timestamps, anomaly_scores, events, train_start, train_end)

    # Compute mean variation for each event
    mean_ratio_partial = partial(mean_ratio, anomaly_scores_healthy=train_data)
    res = data.groupby('event').apply(lambda x: mean_ratio_partial(anomaly_scores_damaged=x['score']),include_groups=False) 
    return res.to_dict()
