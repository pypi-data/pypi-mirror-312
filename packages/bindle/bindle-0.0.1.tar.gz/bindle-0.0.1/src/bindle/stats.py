# TODO
# Some of these should be special classes that can return values and analyses of input data for stats modeling in formats like statsmodels linear regression.
# Maybe covered by that pingouin package.
# What about just knowing stats well and using scipy and statsmodels?

import numpy as np
import pandas as pd
import scipy
from statsmodels.stats.outliers_influence import variance_inflation_factor

def vif_frame(df):
    """Generate a dataframe with VIF for each independent variable.

    Be sure to exclude the dependent variable.
    """
    vif_frame = pd.DataFrame()
    vif_frame["independent_variable"] = df.columns
    vif_frame["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    vif_frame.set_index('independent_variable')
    return vif_frame
