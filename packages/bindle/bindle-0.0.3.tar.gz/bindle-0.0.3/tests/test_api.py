import bindle
import pandas as pd
import pytest

class TestBindleAPI:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_import_bindle(self):
        assert "bindle" in globals()

    def test_data_frane_has_bindle_namespace(self):
        assert hasattr(pd.DataFrame, 'bindle')

    def test_bindle_has_data_namespace(self):
        assert hasattr(pd.DataFrame.bindle, 'data')

    def test_bindle_data_has_read_bigquery(self):
        assert hasattr(pd.DataFrame.bindle.data, 'read_bigquery')

    def test_bindle_data_has_to_bigquery(self):
        assert hasattr(pd.DataFrame.bindle.data, 'to_bigquery')

    def test_bindle_data_has_read_trino(self):
        assert hasattr(pd.DataFrame.bindle.data, 'read_trino')

    def test_bindle_data_has_to_trino(self):
        assert hasattr(pd.DataFrame.bindle.data, 'to_trino')

    def test_bindle_data_has_find_excel_dialog(self):
        assert hasattr(pd.DataFrame.bindle.data, 'find_excel_dialog')

    def test_bindle_data_has_crazy_daisy(self):
        assert hasattr(pd.DataFrame.bindle.data, 'crazy_daisy')

    def test_bindle_has_model_namespace(self):
        assert hasattr(pd.DataFrame.bindle, 'model')

    def test_bindle_has_plot_namespace(self):
        assert hasattr(pd.DataFrame.bindle, 'plot')

    def test_bindle_has_stats_namespace(self):
        assert hasattr(pd.DataFrame.bindle, 'stats')

    def test_bindle_has_wrangle_namespace(self):
        assert hasattr(pd.DataFrame.bindle, 'wrangle')

    def test_bindle_wrangle_has_join_series_as_columns_function(self):
        assert hasattr(pd.DataFrame.bindle.wrangle, 'join_series_as_columns')


class TestBindleModule:

    @classmethod
    def setup_class(cls):
        assert False

    @classmethod
    def teardown_class(cls):
        assert False

    def test_bindle_has_get_connection_function(self):
        assert False

    def test_bindle_has_generate_config_function(self):
        assert False

    def test_bindle_has_make_config_function(self):
        assert False

if __name__ == "__main__":
    pytest.main()
