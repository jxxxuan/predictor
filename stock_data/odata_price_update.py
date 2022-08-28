import pandas as pd
import yfinance as yf
from datetime import timedelta
from datetime import datetime
import utils

#update cdata stock price
def update(cdata=None,write=True):
    nl = pd.read_csv(r'name_list.csv',index_col=0)
    nl['last_update'] = pd.to_datetime(nl['last_update'])
    t = utils.today(5) - timedelta(2,0)
    last_update = nl[(nl['last_update'] < (datetime(t.year,t.month,t.day))) & (nl['status'] == 'odata')]
    
    if len(last_update) == 0:
        print('odata was up-to-date')
        return odata
    
    new_data = []
    new_date = set()
    
    try:
        print('update_process')
        for name in last_update.index:
            print('\t'+name,end=' : ')
            open_ = yf.Ticker(name).history(start=nl.loc[name,'last_update'])['Open']
            print('done')
            new_date = new_date | set(open_.index)
            open_.name = name
            new_data.append(open_)
        
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('updating odata')
        if odata == None:
            print('reading odata.pkl')
            odata = pd.read_pickle(r'odata.pkl')

        new_date = new_date - set(odata.index)
        
        if len(new_date) > 0:
            odata = pd.concat([odata,pd.Series(index=new_date)])
        
        new_data = pd.concat(new_data,axis=1)
        odata.loc[new_data.index,new_data.columns] = new_data
        odata = cdata.sort_index()
        odata = utils.sorting(odata)
        if 0 in odata.columns:
            odata.drop([0],axis=1,inplace=True)
        print(odata)
        
        if write:
            print('writing cdata.pkl')
            odata.to_pickle(r'odata.pkl')
            '''
            Expired : 2022-08-12
            utils.update_last_update(odata=odata)
            utils.update_odata_detail(odata)
            '''
            print('stock price update : complete')
        else:
            return new_data

if __name__ == '__main__':
    update()
