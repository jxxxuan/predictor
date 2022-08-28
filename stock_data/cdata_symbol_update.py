import pandas as pd
import yfinance as yf
import numpy as np
import utils

#update stock symbols
def update():
    nl = pd.read_csv(r'name_list.csv',index_col=0)
    cdata = pd.read_pickle(r'cdata.pkl')
    odata = pd.read_pickle(r'odata.pkl')
    
    new_name_list = set(nl[nl['status'] != 'in list'].index)
    
    if len(new_name_list) == 0:
        print('cdata and sdata was up-to-date')
        return cdata
    
    print(len(new_name_list))
    cdata_list = [cdata]
    odata_list = [odata]
    delisted_sym = []
    
    try:
        print('update_process')
        for name in new_name_list:
            new_data = yf.Ticker(name).history(period='max')[['Close','Open']]
            print(name,end=' : ')
            if new_data.empty:
                print('failure')
                delisted_sym.append(name)
            else:
                print('done')
                if new_data['Close'].count() < 3652:
                    nl.loc[name,'status'] = 'special'
                else:
                    c = new_data['Close']
                    c.name = name
                    o = new_data['Open']
                    o.name = name
                    cdata_list.append(c)
                    odata_list.append(o)
                    nl.loc[name,'status'] = 'in list'
                    nl.loc[name,'count'] = new_data['Close'].count()
                    nl.loc[name,'c_last_valid_index'] = c.last_valid_index()
                    nl.loc[name,'o_last_valid_index'] = o.last_valid_index()
         
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('update data')
        utils.update_delisted_tickers(delisted_sym,nl)
        if not(len(cdata_list) <= 1):
            cdata = pd.concat(cdata_list,axis=1)
            cdata = utils.sorting(cdata)
            odata = pd.concat(odata_list,axis=1)
            odata = utils.sorting(odata)
            print(cdata)
            print(odata)
        else:
            return
        
        print('writing cdata.pkl')
        cdata.to_pickle(r'cdata.pkl')
        odata.to_pickle(r'odata.pkl')
        nl.to_csv(r'name_list.csv')
        utils.update_cdata_detail(cdata)
        utils.update_last_update(cdata)
        print('stock symbols update : complete')

if __name__ == '__main__':
    update()
