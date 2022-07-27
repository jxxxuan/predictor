import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import json
import os
import sys
import re
sys.path.append(r'D:\Documents\code\accuracy')
from spider_utils import utils
from google_news_spider.crawler import gn_page

info = {
    'day':0,
    'month':0,
    'year':2007,
    'start_index':0}
info_path=r'D:\Documents\code\accuracy\reuters_news_data\html\info.json'
errors = []

def update(jump=False):
    if jump:
        info['month']+=1
        info['year'] += info['month'] // 12
        info['month'] = info['month'] % 12
        info['start_index'] = 0
    else:
        info['start_index'] += 10

def write(htmls):
    if  htmls == None or len(htmls) == 0:
        return None
    
    for h in htmls:
        if not os.path.exists(os.path.dirname(h.file_name)):
            os.makedirs(os.path.dirname(h.file_name))
        
        print('file_name: %50s link: %s'%(h.file_name,h.link))
        with open(h.file_name,'w') as f:
            json.dump(h.__dict__,f)

def crawl(htmls):
    if htmls == None or len(htmls) == 0:
        return
    
    for h in htmls:
        print('\t' + h.link,end=': ')
        r = requests.get(h.link,headers={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                          'referer': 'https://www.google.com/',
                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'})
        if r.status_code == 200:
            print('success')
            h.set_html(r.text)
            h.set_id(utils.get_id_form_link('https?://\w+.reuters.com/(.*)$',h.link,1))
            h.set_file_name(utils.get_file_name_from_id(r'D:\Documents\code\accuracy\reuters_news_data\html',h.time,h.id))
            '''
            soup = BeautifulSoup(r.content,'html.parser')
            content = find_content(soup,n.link)
            if content != None:
                n.set_content(content)
                n.set_title(find_title(soup))
                n.set_class(find_class(soup))
            else:
                news.remove(n)
            '''
            time.sleep(random.random()*3)
        else:
            print('fail')
    return htmls
'''
def find_content(soup,link):
    text = ''
    p = soup.find_all('p',class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
    if len(p) > 0:
        for i in p:
            text += '\t' + i.get_text() + '\n\n'
    else:
        text = None
    return text
    
def find_title(soup):
    return soup.find('h1',class_='Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj').get_text()

def find_class(soup):
    return soup.find('a',class_='TextLabel__text-label___3oCVw TextLabel__black-to-orange___23uc0 TextLabel__small-all-caps___2Z2RG ArticleHeader-channel-1DzNK').get_text()

def find_id(link):
    return link
'''

def write_info():
    with open(info_path,'w') as f:
        json.dump(info,f)

def read_info():
    global info
    if os.path.exists(info_path):
        with open(info_path,'r') as f:
            info = json.load(f)
    
if '__main__' == __name__:
    
    read_info()
    g_spider = gn_page('Reuters','Reuters',True)
    while(info['year'] <= 2020 or info['month'] <= 9):
        try:
            print(info)
            write_info()
            news = g_spider(info)
            news = crawl(news)
            write(news)
            if news == None or len(news) <= 0:
                update(True)
            else:
                update()
        except Exception as e:
            errors.append(e)
            if len(errors) > 5:
                with open(r'D:\Documents\code\accuracy\cnn_news_data\html\errors.txt','w') as f:
                    for error in errors:
                        f.write(str(error))
                exit()
