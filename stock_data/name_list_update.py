import pandas as pd
from yahoo_fin import stock_info as si

def delist(nl=None,dl=None):
    if nl == None:
        tickers_list = set(pd.read_csv(r'name_list.csv',index_col=0,squeeze=True))

    if dl == None:
        delisted_tickers = set(pd.read_csv(r'delisted_tickers.csv',index_col=0,squeeze=True))

    pd.Series(list(tickers_list - delisted_tickers),name='symbols').to_csv(r'name_list.csv')
    print('delist complete')
    
def update():
    tickers_list = set(pd.read_csv(r'name_list.csv',index_col=0,squeeze=True))
    tickers_list = tickers_list | set(si.tickers_sp500()) | set(si.tickers_other()) | set(si.tickers_dow()) | set(si.tickers_ftse250()) | set(si.tickers_ibovespa()) | set(si.tickers_niftybank()) | set(si.tickers_nifty50())
    pd.Series(list(tickers_list),name='symbols').to_csv(r'name_list.csv')
    print('update complete')
    
if __name__ == '__main__':
    update()
    delist()
