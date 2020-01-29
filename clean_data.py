import os

import pandas as pd
import itertools as it

from covel import covel_directory_driver, prep_covel


def get_market_data(market_symbol, endswith_field='.txt'):
    directory = covel_directory_driver(market_symbol)
    list_of_files = [file for file in os.listdir(directory) if file.endswith(endswith_field)]
    df = pd.concat([prep_covel(directory + filename, filename) for filename in list_of_files])
    return df.sort_values('Date')


def make_continuous(input_data):
    mod = input_data[['Date', 'Close', 'OpenInt', 'Symbol']]
    foo = pd.pivot_table(mod, index=['Date', 'Symbol'], values=['Close', 'OpenInt'])
    foo.unstack().OpenInt = foo['OpenInt'].ewm(span=5).mean()
    useable_index = pd.DataFrame(foo.unstack().OpenInt.idxmax(axis=1), columns=['Symbol']).reset_index().set_index(['Date', 'Symbol']).index
    return pd.DataFrame(foo.loc[useable_index]).reset_index().set_index('Date')


def fix_quotes(input_data, price_limit, price_fields='Close'):  # <--- was/is specific to GBP; leave for reference in CHF; AD; JPY
    input_data[price_fields] = pd.np.where(input_data[price_fields] > price_limit, (1 / input_data[price_fields]) * 100, (1 / input_data[price_fields]))
    return input_data[price_fields]

