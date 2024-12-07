import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

def score_model(y, yhat, scorers):
    """Score the performance of a model for each of an array of scoring functions (commonly found in `sklearn.metrics`).

    Args:
        y
        yhat
        scorers

    Returns:
        Pandas Series
    """
    score_dict = {f.__name__: f(y, yhat) for f in scorers}
    score_series = pd.Series(score_dict)

    return score_series

def vif_frame(df):
    """Generate a dataframe with VIF for each independent variable.

    Be sure to exclude the dependent variable.
    """
    vif_frame = pd.DataFrame()
    vif_frame["independent_variable"] = df.columns
    vif_frame["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    vif_frame.set_index('independent_variable')
    return vif_frame

