import logging
from functools import wraps
from schwab.auth import Client

import pandas as pd

logger = logging.getLogger(__name__)


def _client_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "_client"):
            error_message = "API client is not set. Use `set_client` to initialize it before using this method."
            raise ValueError(error_message)
        return func(self, *args, **kwargs)

    return wrapper


def _non_array_response_to_array(response):
    data = response.json()
    return [data.get(k) for k in data]

def _convert_time_columns_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    # TODO fix for "realtime" field which may be a boolean indicator
    return df.astype({k: "datetime64[ms]" for k in df.columns[df.columns.str.contains('time', case=False)]})

# Example usage:
# df = df.pipe(convert_time_columns)

@pd.api.extensions.register_dataframe_accessor("chucks")
class ChucksAccessor:
    """Extension to provide more finance dataframe methods."""

    @classmethod
    def set_client(cls, client):

        if not isinstance(client, Client):
            error_message = f"Passed value {client} (type: {type(client)}) is not an instance of {Client}"
            raise ValueError(error_message)

        cls._client = client

        return None

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(response_obj):
        pass

    @staticmethod
    def _convert_datetime_to_ms(df: pd.DataFrame) -> pd.DataFrame:
        return df.astype({"datetime": "datetime64[ms]"})

    @staticmethod
    def _set_index_datetime_symbol(df: pd.DataFrame) -> pd.DataFrame:
        """Sets multiindex with datetime and symbol as the levels.

        Note:
            Removing use of this method from use.
            Too many unneeded complexitiies and blockers to justify.
        """
        return df.set_index(["datetime", "symbol"])

    @staticmethod
    def read_candles(price_history_responses):
        """Returns a dataframe of the candles responses.

        Can take multiple responses and output one df.

        Args:
            price_history_responses (iterable): An iterable of price history responses.

        """
        return (
            pd.concat(
                pd.json_normalize(
                    c.json(), record_path="candles", meta=["symbol", "empty"]
                )
                for c in price_history_responses
            )
            .pipe(ChucksAccessor._convert_datetime_to_ms)
            .set_index("datetime")
        )

    @staticmethod
    def read_accounts(accounts_response):
        return (
            pd.json_normalize(accounts_response.json(), sep="_")
            .set_index("securitiesAccount_accountNumber", drop=False)
            .rename_axis(index="accountNumber")
        )

    @staticmethod
    def read_movers(movers_response):
        return pd.json_normalize(
            movers_response.json(), record_path="screeners"
        ).set_index("symbol", drop=False)

    @staticmethod
    def read_instruments(instruments_response):
        return pd.json_normalize(
            instruments_response.json(), record_path="instruments", sep="_"
        ).set_index("symbol", drop=False)

    @staticmethod
    def read_quotes(quotes_response):
        return pd.json_normalize(
            _non_array_response_to_array(quotes_response), sep="_"
        ).set_index("symbol", drop=False)

    @_client_required
    def get_quotes(self):
        symbols = self._get_unique_symbols_from_index()
        response = self._client.get_quotes(symbols)
        data_array = _non_array_response_to_array(response)

        return pd.json_normalize(data_array, sep="_").set_index("symbol", drop=False)

    @_client_required
    def get_fundamentals(self):
        symbols = self._get_unique_symbols_from_index()
        response = self._client.get_instruments(
            symbols, self._client.Instrument.Projection.FUNDAMENTAL
        )

        return self.read_instruments(response)


    @_client_required
    def get_price_history(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_day(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_day(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_fifteen_minutes(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_fifteen_minutes(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_five_minutes(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_five_minutes(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_minute(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_minute(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_ten_minutes(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_ten_minutes(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_thirty_minutes(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_thirty_minutes(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    @_client_required
    def get_price_history_every_week(self, *args, **kwargs):
        """Get price history.
        
        Additional args and kwargs are passed to the schwab client method.
        """
        symbols = self._get_unique_symbols_from_index()
        responses = (self._client.get_price_history_every_week(s, *args, **kwargs) for s in symbols)
        return self.read_candles(responses)

    def _get_unique_symbols_from_index(self):
        return self._obj.index.get_level_values("symbol").unique()

    def what_about_adding_field_like_response_type_to_df(self):
        pass

    def generate_price_history_features(self):
        pass
