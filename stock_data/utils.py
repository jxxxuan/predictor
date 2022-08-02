import pandas as pd
import yfinance as yf
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

'''
expired : 01-08-22
def update_name_list():
    tickers_list = set(pd.read_csv(r'name_list.csv',index_col=0)['symbols'])
    delisted_tickers = set(pd.read_csv(r'delisted_tickers.csv',index_col=0)['delisted_symbols'])
    tickers_list = tickers_list | set(si.tickers_sp500()) | set(si.tickers_other()) | set(si.tickers_dow()) | set(si.tickers_ftse250()) | set(si.tickers_ibovespa()) | set(si.tickers_niftybank()) | set(si.tickers_nifty50())
    tickers_list = tickers_list - delisted_tickers
    pd.DataFrame(list(tickers_list),columns=['symbols']).to_csv(r'name_list.csv')
    print('complete')
'''

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


def update_delisted_tickers(delisted_sym,name_list):
    if len(delisted_sym) == 0:
        return
    
    delisted_sym = name_list.loc[delisted_sym]
    name_list = name_list.drop(delisted_sym.index)
    delisted_sym = pd.concat([delisted_sym,pd.read_csv(r'delisted_tickers.csv',index_col=0)])

    delisted_sym.to_csv(r'delisted_tickers.csv')
    name_list.to_csv(r'name_list.csv')

def today(utc):
    return datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=utc)))

def area(cdata):
    area = pd.Series(range(1,len(cdata.columns)+1)) * cdata.count()
    area.plot()

def count(cdata):
    cdata.count().plot()
'''
if __name__ == '__main__':
    nl = pd.read_csv(r'name_list.csv')
    dl = pd.read_csv(r'delisted_tickers.csv')
    update_delisted_tickers(dl,nl)
'''
