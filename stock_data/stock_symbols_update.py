import pandas as pd
import yfinance as yf
import utils

def update(cdata=None,write=True):
    name_list = pd.read_csv(r'name_list.csv',index_col=0,squeeze=True)
    
    if cdata == None:
        print('reading cdata.csv')
        cdata = pd.read_csv(r'cdata.csv',index_col=0)
        cdata = cdata.astype('float32')
        cdata.index = pd.DatetimeIndex(cdata.index)

    print('reading sdata.csv')
    sdata = pd.read_csv(r'sdata.csv',index_col=0,squeeze=True)
    
    new_name_list = set(name_list) - set(cdata.columns) - set(sdata.index)
    if len(new_name_list) == 0:
        print('cdata and sdata was up to date')
        return cdata
    
    print(len(new_name_list))
    cdata_list = [cdata]
    delisted_sym = set()
    
    try:
        for name in new_name_list:
            print(name,end=' : ')
            new_data = yf.Ticker(name).history(period='max')['Close']
            if new_data.empty:
                print('failure')
                delisted_sym.add(name)
            else:
                print('done')
                new_data.name = name
                if new_data.count() < 300:
                    sdata[name] = new_data.count()
                else:
                    cdata_list.append(new_data)
        
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print('update process')
        utils.update_delisted_tickers(delisted_sym,new_name_list)
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
        else:
            return cdata,sdata

if __name__ == '__main__':
    update()
