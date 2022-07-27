import pandas as pd
import datetime
import yfinance as yf
import last_update as lu
import utils

#update cdata stock price
def update(cdata=None,write=True):
    last_update = pd.read_csv(r'last_update.csv',index_col=0,squeeze=True)
    last_update = last_update[last_update != utils.today(5)]
    
    if len(last_update) == 0:
        print('cdata was up-to-date')
        return cdata
    
    if cdata == None:
        print('reading cdata.csv')
        cdata = pd.read_csv(r'cdata.csv',index_col=0)
        cdata = cdata.astype('float32')
        cdata.index = pd.DatetimeIndex(cdata.index)

    last_update = last_update[cdata.columns]
    if len(last_update) == 0:
        print('cdata was up-to-date')
        return cdata
    
    try:
        print('update_process')
        new_data_list = []
        print(cdata)
        
        for name in last_update.index:
            print('\t'+name,end=' : ')
            close = yf.Ticker(name).history(start=last_update[name])['Close']
            print('done')
            close.name = name
            new_data_list.append(close)
        
    except KeyboardInterrupt as e:
        print('terminate command')
    finally:
        print('updating cdata')
        new_data = pd.concat(new_data_list,axis=1)
        cdata = cdata.reindex((pd.DatetimeIndex(set(new_data.index) | set(cdata.index))).sort_values())
        cdata.update(new_data,overwrite=False)
        cdata = utils.sorting(cdata)
        print(cdata)
        
        if write:
            print('writing cdata.csv')
            cdata = cdata.astype('float32')
            cdata.to_csv(r'cdata.csv')
            lu.update(cdata=cdata)
            print('stock price update : complete')
        return new_data
        raise

if __name__ == '__main__':
    update()
