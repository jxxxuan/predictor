import requests
import pandas as pd
import os
import time
from random import random
import json

def write(link,text):
    t = nl.loc[link,'time'].to_pydatetime()
    folder_name = r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data\html' + t.strftime('\\%Y\%m')
    file_name = folder_name + t.strftime('\\%d.txt')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if not os.path.exists(file_name):
        with open(file_name,'a') as f:
            f.write('[')
            f.write(json.dumps({'link':link,'html':text}))
    
    with open(file_name,'a') as f:
        f.write(',')
        f.write(json.dumps({'link':link,'html':text}))
        '''with open(file_name,'r') as f:
            l = json.loads(f.read())'''
        opened_file.append(file_name)
        nl.loc[link,'html_file_path'] = file_name
    

if __name__ == '__main__':
    nl = pd.read_csv(r'name_list.csv',index_col=0)
    opened_file = []
    nl['time'] = nl['time'].astype('datetime64')
    links = nl[nl['html_file_path'].isna()].index
    print(len(links))
    try:
        for l in links:
            print(l,end=' : ')
            res = requests.get(l,headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'})
            write(l,res.text)
            print('done')
            time.sleep(random() * 5)
            
    except KeyboardInterrupt as e:
        print(e)
    finally:
        for n in opened_file:
            with open(n,'a') as f:
                f.write(']')
        nl.to_csv(r'name_list.csv')
