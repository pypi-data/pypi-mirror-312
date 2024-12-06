import pandas as pd
import pytest

import chucks


class TestChucksAccessor:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_import_chucks(self):
        assert "chucks" in globals()

    def test_dataframe_has_chucks_accessor(self):
        assert hasattr(pd.DataFrame, "chucks")

    def test_chucks_accessor_has_read_candles(self):
        assert hasattr(pd.DataFrame.chucks, "read_candles")

    def test_chucks_accessor_has_read_instruments(self):
        assert hasattr(pd.DataFrame.chucks, "read_instruments")

    def test_chucks_accessor_has_read_accounts(self):
        assert hasattr(pd.DataFrame.chucks, "read_accounts")

    def test_chucks_accessor_has_read_movers(self):
        assert hasattr(pd.DataFrame.chucks, "read_movers")

    def test_chucks_read_candles_is_callable(self):
        assert callable(pd.DataFrame.chucks.read_candles)

    def test_chucks_read_instrument_is_callable(self):
        assert callable(pd.DataFrame.chucks.read_instruments)

    def test_chucks_read_accounts_is_callable(self):
        assert callable(pd.DataFrame.chucks.read_accounts)

    def test_chucks_read_movers_is_callable(self):
        assert callable(pd.DataFrame.chucks.read_movers)

    def test_chucks_has_private_method_convert_datetime_to_ms(self):
        assert hasattr(pd.DataFrame.chucks, "_convert_datetime_to_ms")

    def test_chucks_has_private_method_set_index_datetime_symbol(self):
        assert hasattr(pd.DataFrame.chucks, "_set_index_datetime_symbol")

    def test_chucks_has_plot_attribute(self):
        assert hasattr(pd.DataFrame.chucks, "plot")

    def test_chucks_has_model_attribute(self):
        assert hasattr(pd.DataFrame.chucks, "model")

    def test_chucks_has_trader_attribute(self):
        assert hasattr(pd.DataFrame.chucks, "trader")

    def test_chucks_has_market_data_attribute(self):
        assert hasattr(pd.DataFrame.chucks, "market_data")


class TestChucksModule:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_import_chucks(self):
        assert "chucks" in globals()

    def test_chucks_has_private_function_client_required(self):
        assert hasattr(chucks, "_client_required")

    def test_chucks_private_function_client_is_callable(self):
        assert callable(chucks._client_required)


if __name__ == "__main__":
    pytest.main()
