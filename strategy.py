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


def strategy(input_data, fast_ema=42, slow_ema=252):
    input_data['fast_ma'] = input_data['Close'].ewm(span=fast_ema, adjust=False).mean()
    input_data['slow_ma'] = input_data['Close'].ewm(span=slow_ema, adjust=False).mean()
    input_data['Passive_Returns'] = pd.np.log(input_data['Close'] / input_data['Close'].shift(1))
    input_data['Position'] = pd.np.where(input_data['fast_ma'] > input_data['slow_ma'], 1, -1)
    input_data['Strategy_Returns'] = input_data['Position'].shift(1) * input_data['Passive_Returns']
    input_data['Passive'] = input_data['Passive_Returns'].cumsum().apply(pd.np.exp)
    input_data['Strategy'] = input_data['Strategy_Returns'].cumsum().apply(pd.np.exp)
    return input_data


def brute_force_strategy(input_data):   # FIXME

    def brute_force(input_data, fast_ma, slow_ma):
        input_data['fast_ma'] = input_data['Close'].ewm(span=fast_ma, adjust=False).mean()
        input_data['slow_ma'] = input_data['Close'].ewm(span=slow_ma, adjust=False).mean()
        input_data['Passive_Returns'] = pd.np.log(input_data['Close'] / input_data['Close'].shift(1))
        input_data['Position'] = pd.np.where(input_data['fast_ma'] > input_data['slow_ma'], 1, -1)
        input_data['Strategy_Returns'] = input_data['Position'].shift(1) * input_data['Passive_Returns']
        input_data['Passive'] = input_data['Passive_Returns'].cumsum().apply(pd.np.exp)
        input_data['Strategy'] = input_data['Strategy_Returns'].cumsum().apply(pd.np.exp)
        return input_data

    for fast_ma, slow_ma in it.product(range(10, 31, 5), range(50, 101, 10)):
        res = brute_force(input_data, fast_ma, slow_ma)
        results = pd.append(pd.DataFrame({'Fast': fast_ma, 'Slow': slow_ma, 'CReturns': res['CReturns'],
                                               'CStrategy': res['CStrategy']}, index=[0]), ignore_index=True)

    annual_vol = input_data[['Passive', 'Strategy']].std() * 252 ** 0.5
    ema_pair = results['Strategy'].idxmax()

    return f'The annual volatility is {annual_vol} and the highest return is {ema_pair}'
