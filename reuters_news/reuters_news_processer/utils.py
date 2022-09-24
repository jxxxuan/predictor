import os
import re
import json
import numpy as np
from bs4 import BeautifulSoup

def get_reuters_news(f):
    files = []
    for year in os.listdir(r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data'+'\\'+f):
        folder = r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data'+'\\'+f+'\\'+year
        for month in os.listdir(folder):
            for day in os.listdir(folder + '\\' + month):
                files.append({"file_name":folder + '\\' + month + '\\' + day,"day":day[:2],"month":month,"year":year})
    return files

if __name__ == '__main__':
    pass
    
