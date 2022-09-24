import pandas as pd
import sys
from datetime import datetime
from time import sleep
import random
import json
sys.path.append(r'D:\Documents\predictor\google_search_engine')
from google_news_engine import gn_engine

if __name__ == '__main__':
    nl = pd.read_csv(r'name_list.csv',index_col=0)
    nl['time'] = nl['time'].astype('datetime64')
    
    with open('index.json','r') as f:
        index = json.load(f)

    gne = iter(gn_engine('Reuters','Reuters',datetime(index['year'],index['month'],index['day']),index['index']))
    l = [nl]
    try:
        while True:
            links = next(gne)
            if links[-1]['time'] != None and links[-1]['time'] >= datetime(2022,8,30):
                print('name_list was update-to-date')
                break
            else:
                print('date : ',links[-1]['time'])
            
            for link in links:
                d = pd.DataFrame(link,index=[link['link']],columns=['time','google_link','file_path'])
                l.append(d)
                print('link : ',link['link'])
            sleep(random.random() * 5)
        
    except KeyboardInterrupt as e:
        print(e)
    finally:
        print('concat name list')
        nl = pd.concat(l)
        nl.index.name = 'link'
        nl = nl.reset_index().drop_duplicates(['link']).set_index('link')
        nl.to_csv(r'name_list.csv')
        with open('index.json', 'w') as f:
            json.dump(gne.get_index(), f)
