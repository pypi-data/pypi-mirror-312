# LUMO Damage Detection Evaluation Package

This package provides a standardized framework for evaluating damage detection and localization strategies using the LUMO dataset. Users can input timestamps alongside their corresponding anomaly indices, and the package computes various performance scores for each damage case, promoting consistency in damage detection evaluation.

## Features

- **Standardized Evaluation Metrics**: Calculates TPR and FPR at a threshold set such as FPR for training data is 1%. 
The training dataset should be only the first moth of data
- **Damage Case Analysis**: Provides detailed performance evaluations for each specific damage scenario within the LUMO dataset.


## Installation

To install the package, run:

```bash
pip install lumo-eval
