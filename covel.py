import pandas as pd


def covel_directory_driver(market_symbol):
    if market_symbol.lower() == 'australian_dollar':
        return 'data/historical/australian_dollar/'
    if market_symbol.lower() == 'british_pound':
        return 'data/historical/british_pound/'
    if market_symbol.lower() == 'cac40':
        return 'data/historical/cac40/'
    if market_symbol.lower() == 'coffee':
        return 'data/historical/coffee/'
    if market_symbol.lower() == 'corn':
        return 'data/historical/corn/'
    if market_symbol.lower() == 'cotton':
        return 'data/historical/cotton/'
    if market_symbol.lower() == 'crb_index':
        return 'data/historical/crb_index/'
    if market_symbol.lower() == 'crude':
        return 'data/historical/crude/'
    if market_symbol.lower() == 'dollar_index':
        return 'data/historical/dollar_index/'
    if market_symbol.lower() == 'euro_dollar':
        return 'data/historical/euro_dollar/'
    if market_symbol.lower() == 'feeder_cattle':
        return 'data/historical/feeder_cattle/'
    if market_symbol.lower() == 'gilt':
        return 'data/historical/gilt/'
    if market_symbol.lower() == 'gold':
        return 'data/historical/gold/'
    if market_symbol.lower() == 'heating_oil':
        return 'data/historical/heating_oil/'
    if market_symbol.lower() == 'hg_copper':
        return 'data/historical/hg_copper/'
    if market_symbol.lower() == 'live_hogs':
        return 'data/historical/live_hogs/'
    if market_symbol.lower() == 'oats':
        return 'data/historical/oats/'
    if market_symbol.lower() == 'orange_juice':
        return 'data/historical/orange_juice/'
    if market_symbol.lower() == 'palladium':
        return 'data/historical/palladium/'
    if market_symbol.lower() == 'platinum':
        return 'data/historical/platinum/'
    if market_symbol.lower() == 'pork_bellies':
        return 'data/historical/pork_bellies/'
    if market_symbol.lower() == 'silver':
        return 'data/historical/silver/'
    if market_symbol.lower() == 'soy':
        return 'data/historical/soy/'
    if market_symbol.lower() == 'sp500':
        return 'data/historical/sp500/'
    if market_symbol.lower() == 'sterling':
        return 'data/historical/sterling/'
    if market_symbol.lower() == 'sugar':
        return 'data/historical/sugar/'
    if market_symbol.lower() == 'swiss_franc':
        return 'data/historical/swiss_franc/'
    if market_symbol.lower() == 't_bills':
        return 'data/historical/t_bills/'
    if market_symbol.lower() == 'wheat':
        return 'data/historical/wheat/'
    if market_symbol.lower() == 'yen':
        return 'data/historical/yen/'
    if market_symbol.lower() == 'canadian_dollar':
        return 'data/historical/canadian_dollar/'
    if market_symbol.lower() == 'error_test':
        return 'data/error_tests/'
    if market_symbol.lower() == 'test_data':
        return 'data/test_data/'
    return

def prep_covel(relative_path, filename):
    try:
        df = pd.read_csv(relative_path).assign(Symbol=filename.replace('.txt', ''))
        # you could try to add a check here whether the date column contains "/" and how long the value is (this will help with the 2000 problem)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    except KeyError:
        # converters={'Date': lambda x: str(x)} prevents 3 leading zeros being dropped from 000101 (Jan 1, 2000)
        df = pd.read_csv(relative_path,
                         names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'OpenInt'], converters={'Date': lambda x: str(x)}). \
            assign(Symbol=filename.replace('.txt', ''))
        df['Date'] = pd.to_datetime(df['Date'], format='%y%m%d')
    # adjust for date mapping issues: values 69–99 are mapped to 1969–1999, and values 0–68 are mapped to 2000–2068.
    df.loc[df['Date'].dt.year >= 2058, 'Date'] = df.loc[df['Date'].dt.year >= 2058, 'Date'] - pd.np.timedelta64(100, 'Y')
    return df