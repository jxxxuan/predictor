import pandas as pd
import yfinance as yf
import numpy as np
import utils

#update stock symbols
def update(odata=None,write=True):
    nl = pd.read_csv(r'odata_name_list.csv',index_col=0)

    name_list = set(nl[nl['status'] != 'done'].index)
    
    print(len(name_list))
    odata_list = []
    
    try:
        print('update_process')
        for name in name_list:
            new_data = yf.Ticker(name).history(period='max')['Open']
            print(name,end=' : ')
            if new_data.empty:
                print('failure')
            else:
                print('done')
                nl.loc[name,'status'] = 'done'
                new_data.name = name
                if new_data.count() < 3652:
                    pass
                else:
                    odata_list.append(new_data)
         
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('update data')
        if odata == None:
            print('reading odata.pkl')
            odata = pd.read_pickle(r'odata.pkl')
            odata_list.append(odata)
        if not(len(odata_list) <= 1):
            odata = pd.concat(odata_list,axis=1)
            odata = utils.sorting(odata)
            print(odata)
        else:
            return
        
        if write:
            print('writing odata.pkl')
            odata.to_pickle(r'odata.pkl')
            nl.to_csv('odata_name_list.csv')
            print('stock symbols update : complete')
        else:
            return odata,sdata

if __name__ == '__main__':
    update()
