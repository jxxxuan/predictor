import os
import re
import json
import numpy as np
from bs4 import BeautifulSoup

def get_files(f):
    files = []
    for year in os.listdir(f):
        folder = f+'\\'+year
        for month in os.listdir(folder):
            for day in os.listdir(folder + '\\' + month):
                files.append({"file_name":folder + '\\' + month + '\\' + day,"day":day[:2],"month":month,"year":year})
    return files

def remove_duplicates(f):
    files = get_files(f)
    for file in files:
        with open(file['file_name'],'r') as f:
            try:
                data = json.loads(f.read())
            except json.decoder.JSONDecodeError as e:
                print(file['file_name'])

        l = [i['link'] for i in data]
        s = set(l)
        print(file)
        if len(s) == len(l):
            continue
        else:
            print(file['file_name'])
            v = []
            for link in s:
                v.append(l.index(link))
            r = set(range(len(l))) - set(v)
            for i in r:
                data[i] = None
            for i in range(len(r)):
                data.remove(None)
                
            with open(file['file_name'],'w') as f:
                f.write(json.dumps(data))

if __name__ == '__main__':
    get_reuters_news(r'D:\Documents\predictor\data\reuters_news\data')
    
    
