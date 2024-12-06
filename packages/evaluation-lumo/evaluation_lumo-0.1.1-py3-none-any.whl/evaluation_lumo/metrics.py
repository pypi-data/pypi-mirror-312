import numpy as np
import pandas as pd
import warnings
from sys import float_info
eps = float_info.epsilon



def compute_tr(anomaly_scores:np.ndarray | pd.Series, threshold:float) -> float:
    """
    Compute the Trigger Rate (TPR/FPR) given anomaly scores and a threshold.

    Parameters:
    - anomaly_scores (array-like): Anomaly index scores.
    - threshold (float): Threshold above which scores are considered anomalies.

    Returns:
    - float: Trigger Rate.
    """
    print(anomaly_scores)
    if isinstance(anomaly_scores, pd.Series):
        anomaly_scores = anomaly_scores.values
    if isinstance(anomaly_scores, list):
        anomaly_scores = np.array(anomaly_scores)

    return np.sum(anomaly_scores > threshold) / len(anomaly_scores)

def mean_ratio(anomaly_scores_healthy: np.ndarray | pd.Series, anomaly_scores_damaged: np.ndarray | pd.Series) -> float:
    """
    Compute the mean ratio of anomaly scores between healthy and damaged states.

    Parameters:
    - anomaly_scores_healthy (array-like): Anomaly index scores for healthy state.
    - anomaly_scores_damaged (array-like): Anomaly index scores for damaged state.

    Returns:
    - float: Mean ratio of anomaly scores.
    """
    if isinstance(anomaly_scores_healthy, pd.Series):
        anomaly_scores_healthy = anomaly_scores_healthy.values
    if isinstance(anomaly_scores_damaged, pd.Series):
        anomaly_scores_damaged = anomaly_scores_damaged.values
    if isinstance(anomaly_scores_healthy, list):
        anomaly_scores_healthy = np.array(anomaly_scores_healthy)
    if isinstance(anomaly_scores_damaged, list):
        anomaly_scores_damaged = np.array(anomaly_scores_damaged)
    
    # Compute the range of healthy scores
    range_healthy = np.max(anomaly_scores_healthy) - np.min(anomaly_scores_healthy)

    # Handle zero range by raising a warning and using a range of 1
    if range_healthy == 0:
        warnings.warn(
            "Range of healthy anomaly scores is 0. Using a fallback range of 1.",
            UserWarning
        )
        range_healthy = 1

    # Compute the mean ratio
    res = np.mean(anomaly_scores_damaged) / (np.mean(anomaly_scores_healthy)+eps) / (range_healthy+eps)
    return res