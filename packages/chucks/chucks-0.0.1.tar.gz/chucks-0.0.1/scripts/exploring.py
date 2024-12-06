import pandas as pd
import chucks
from chucks.utils import get_schwab_client

if __name__ == "__main__":
    c = get_schwab_client()
    chucks.ChucksAccessor.set_client(c)

    df = pd.DataFrame.chucks.read_candles([c.get_price_history_every_day('$SPX')])
