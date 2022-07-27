import pandas as pd

#update last index for each stcok
def update(cdata=pd.DataFrame(),write=True):
    if len(cdata) == 0:
        print('reading cdata.csv')
        cdata = pd.read_csv(r'cdata.csv',index_col=0)
        cdata = cdata.astype('float32')
        cdata.index = pd.DatetimeIndex(cdata.index)

    last_update = pd.read_csv('last_update.csv',index_col=0,squeeze=True)
    try:
        print('update process')
        new_data_list = dict()

        for name in cdata.columns:
            new_data_list[name] = cdata[name].last_valid_index()
            
    except KeyboardInterrupt as e:
        print('terminate')
    finally:
        last_update.update(pd.Series(new_data_list,name='last_update',dtype='datetime64[ns]'))
        last_update = pd.to_datetime(last_update)
        print(last_update)
        if write:
            print('writing last_update.csv')
            last_update.to_csv(r'last_update.csv')
            print('last update : complete')
        return last_update

if __name__ == '__main__':
    update()
