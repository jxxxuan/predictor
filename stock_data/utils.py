import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
import datetime

def sorting(cdata):
    return cdata[cdata.count().sort_values(ascending=False).index]
    
def update_bsdata(new_df,data_type,df=None,write=True):
    if df == None:
        print('reading...')
        if data_type == 'sdata':
            df = pd.read_csv(r'sdata.csv',index_col=0)
        elif data_type == 'bdata':
            df = pd.read_csv(r'bdata.csv',index_col=0)
        df.index = pd.DatetimeIndex(df.index)
        
    print('update_process')
    df.update(new_df)

    if write:
        df.to_csv(data_type+'.csv')
    else:
        return df

def update_name_list():
    tickers_list = set(pd.read_csv(r'name_list.csv',index_col=0)['symbols'])
    delisted_tickers = set(pd.read_csv(r'delisted_tickers.csv',index_col=0)['delisted_symbols'])
    tickers_list = tickers_list | set(si.tickers_sp500()) | set(si.tickers_other()) | set(si.tickers_dow()) | set(si.tickers_ftse250()) | set(si.tickers_ibovespa()) | set(si.tickers_niftybank()) | set(si.tickers_nifty50())
    tickers_list = tickers_list - delisted_tickers
    pd.DataFrame(list(tickers_list),columns=['symbols']).to_csv(r'name_list.csv')
    print('complete')
    
'''
def count_bdata(df):
    l = []
    for name in df.columns:
        d = df[name]
        d = d[d.first_valid_index():d.last_valid_index()]
        l.append(d[d.isna()].sum())
    df = pd.DataFrame([[l],df.count()],index=['len_of_na','count'],columns=df.columns)

def count_sdata(df):
    return pd.DataFrame([list(df.count())],index=['count'],columns=df.columns)
'''

def update_delisted_tickers(delisted_sym,tickers_list):
    if len(delisted_sym) == 0:
        return
    
    df = set(pd.read_csv(r'delisted_tickers.csv',index_col=0,squeeze=True))
    print(len(df))
    print(len(delisted_sym))
    df = df | delisted_sym
    print(len(df))
    df = pd.Series(list(df),name='symbols')
    df.to_csv(r'delisted_tickers.csv')

    tickers_list = tickers_list - delisted_sym
    pd.Series(list(tickers_list),name='symbols').to_csv(r'name_list.csv')

def today(utc):
    return datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=utc)))



'''
if __name__ == '__main__':
    d = update()
'''
