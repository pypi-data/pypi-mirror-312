import pandas as pd
import numpy as np

@pd.api.extensions.register_dataframe_accessor("bindle")
class BindleAccessor:
    "Bindle Pandas Extensions."

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @staticmethod
    def from_drv(rv, function_method):
        """Quickly create a one-column dataframe from a scipy discrete random variable."""

        m = getattr(rv, function_method)
        df = pd.DataFrame([(i, m(i)) for i in np.arange(rv.args[0])]).set_index(0).rename_axis('x').rename(columns={1: function_method})
        return df

    @staticmethod
    def from_crv(rv, function_method, np_linspace_tuple):
        """Quickly create a one-column dataframe from a scipy continuous random variable."""

        m = getattr(rv, function_method)
        df = pd.DataFrame([(i, m(i)) for i in np.linspace(*np_linspace_tuple)]).set_index(0).rename_axis('x').rename(columns={1: function_method})
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
