import pandas as pd
import yfinance as yf
import utils

def update(cdata=None,write=True):
    name_list = pd.read_csv(r'name_list.csv',index_col=0)
    sdata = pd.read_csv(r'sdata.csv',index_col=0,squeeze=True)
    
    if cdata == None:
        print('reading cdata.csv')
        names = pd.read_csv(r'cdata.csv',index_col=0,nrows=0)
        names = dict.fromkeys(names, 'float32')
        names['index'] = 'datetime64'
        cdata = pd.read_csv(r'cdata.csv',index_col=0,dtype = names)
    
    new_name_list = set(name_list.index) - set(cdata.columns) - set(sdata.index)
    if len(new_name_list) == 0:
        print('cdata and sdata was up to date')
        return cdata
    
    print(len(new_name_list))
    cdata_list = [cdata]
    delisted_sym = []
    
    try:
        for name in new_name_list:
            print(name,end=' : ')
            new_data = yf.Ticker(name).history(period='max')['Close']
            if new_data.empty:
                print('failure')
                delisted_sym.append(name)
            else:
                print('done')
                new_data.name = name
                if new_data.count() < 3652:
                    sdata[name] = new_data.count()
                else:
                    cdata_list.append(new_data)
        
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('update process')
        utils.update_delisted_tickers(delisted_sym,name_list)
        if not(len(cdata_list) <= 1):
            cdata = pd.concat(cdata_list,axis=1)
            cdata = cdata.astype('float32')
            print(cdata.sample(10,axis=1).tail(10))
            print(cdata)
        else:
            return
        
        if write:
            cdata.to_csv(r'cdata.csv')
            sdata.to_csv(r'sdata.csv')
            update_cdata_detail(cdata)
        else:
            return cdata,sdata

if __name__ == '__main__':
    update()
