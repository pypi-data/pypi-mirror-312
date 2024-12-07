import pandas as pd
import numpy as np

@pd.api.extensions.register_dataframe_accessor("bindle")
class BindleAccessor:
    "Bindle Pandas Extensions."

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @staticmethod
    def from_drv(drv, distribution_function):
        """Create a one-column dataframe from a scipy discrete random variable.

        Args:
            drv: A scipy discrete random variable.
            distribution_function: Name of the `scipy.stats.random_variable` method to generate `y`.

        Returns:
            Pandas DataFrame
        """

        m = getattr(drv, distribution_function)
        df = pd.DataFrame([(i, m(i)) for i in np.arange(drv.args[0])]).set_index(0).rename_axis('x').rename(columns={1: distribution_function})
        return df

    @staticmethod
    def from_crv(crv, distribution_function, np_linspace_tuple):
        """Create a one-column dataframe from a scipy continuous random variable.

        Args:
            crv: A scipy continuous random variable.
            distribution_function: Name of the `scipy.stats.random_variable` method to generate `y`.
            np_linspace_tuple (tuple): The argument to `np.linspace` as a tuple. Min, Max, and Size.

        Returns:
            Pandas DataFrame
        """

        m = getattr(crv, distribution_function)
        df = pd.DataFrame([(i, m(i)) for i in np.linspace(*np_linspace_tuple)]).set_index(0).rename_axis('x').rename(columns={1: distribution_function})
        return df

    def convert_columns_to_type(self, *args, dtype=None, **kwargs):
        if dtype is None:
            raise ValueError("The 'dtype' parameter must be specified.")

        # Create the dictionary comprehension for the columns
        type_mapping = {column: dtype for column in args}

        # Use astype with the mapping and additional kwargs
        return self._obj.astype(type_mapping, **kwargs)

    def assign_group_transform(self, new_column_name, groupby_key, function):
        pass

        # df = self._obj.assign({new_column_name: self._obj.groupby(groupby_key).transform(function)})
        
        # return df
