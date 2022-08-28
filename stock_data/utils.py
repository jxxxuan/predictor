import pandas as pd
import yfinance as yf
import datetime

def sorting(cdata):
    return cdata[cdata.count().sort_values(ascending=False).index]

def update_delisted_tickers(delisted_sym,name_list):
    if len(delisted_sym) == 0:
        return
    
    name_list.loc[delisted_sym,'status'] = 'delisted'
    name_list.to_csv(r'name_list.csv')

def today(utc=0):
    return datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=utc)))

def update_cdata_detail(cdata,detail=None,image=True):
    print('update cdata details')

    print(cdata)
    detail = pd.DataFrame(data = {'x' : range(1,len(cdata.columns)+1), 'y' : cdata.count()},index=cdata.columns)
    detail['area'] = detail['y'] * detail['x']
    print(detail)
    detail.to_csv(r'train_details.csv')
    detail.plot().get_figure().savefig(r'train_area.jpg')
    
def count(cdata):
    cdata.count().plot().get_figure().savefig(r'count_train.jpg')

def update_last_update(cdata = None,write=True):
    if cdata is None:
        raise Exception('cdata is None')
    
    nl = pd.read_csv('name_list.csv',index_col=0)
    try:
        print('update process')
        for name in cdata.columns:
            nl.loc[name,'last_update'] = cdata[name].last_valid_index()
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        print(nl)
        if write:
            nl.to_csv(r'name_list.csv')
            print('last update : complete')
        return nl

if __name__ == '__main__':
    cdata = pd.read_pickle(r'cdata_got_sector.pkl')
    update_cdata_detail(cdata)
