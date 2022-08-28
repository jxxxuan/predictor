import pandas as pd
import yfinance as yf
from datetime import timedelta
from datetime import datetime
import utils

#update cdata stock price
def update():
    nl = pd.read_csv(r'name_list.csv',index_col=0)
    nl['last_valid_index'] = pd.to_datetime(nl['last_valid_index'])
    t = utils.today(5) - timedelta(2,0)
    last_valid_index = nl[(nl['last_valid_index'] < (datetime(t.year,t.month,t.day))) & (nl['status'] == 'in list')]
    
    if len(last_valid_index) == 0:
        print('data was up-to-date')
    
    new_data = []
    cdata = pd.read_pkl(r'C:\Users\Windows\Documents\GitHub\predictor\stock_data\cdata.pkl')
    odata = pd.read_pkl(r'C:\Users\Windows\Documents\GitHub\predictor\stock_data\odata.pkl')
    cdata_list = []
    odata_list = []
    new_date = set()
    
    try:
        print('update_process')
        for name in last_valid_index.index:
            print('\t'+name,end=' : ')
            new_data = yf.Ticker(name).history(start=nl.loc[name,'last_valid_index'])[['Close','Open']]
            print('done')
            new_date = new_date | set(close.index)
            close = new_data['Close']
            close.name = name
            open_ = new_data['Open']
            open_.name = name
            cdata_list.append(close)
        
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('updating cdata')
        new_date = new_date - set(cdata.index)
        if len(new_date) > 0:
            cdata = pd.concat([cdata,pd.Series(index=new_date)])
        
        new_data = pd.concat(new_data,axis=1)
        cdata.loc[new_data.index,new_data.columns] = new_data
        cdata = cdata.sort_index()
        cdata = utils.sorting(cdata)
        if 0 in cdata.columns:
            cdata.drop([0],axis=1,inplace=True)
        print(cdata)
        
        if write:
            print('writing cdata.pkl')
            cdata.to_pickle(r'cdata.pkl')
            utils.update_last_update(cdata=cdata)
            utils.update_cdata_detail(cdata)
            print('stock price update : complete')
        else:
            return new_data

if __name__ == '__main__':
    update()
