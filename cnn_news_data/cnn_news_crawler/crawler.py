import requests
from bs4 import BeautifulSoup
import sys
import random
import time
import os
import json
import re
import calendar

sys.path.append(r'D:\Documents\code\predictor')
from google_news_spider.crawler import gn_page
from spider_utils import utils

name = 'CNN'
info_path = r'D:\Documents\code\predictor\cnn_news_data\html\info.json'
info = {'year':2003,
        'month':9,
        'day':0,
        'start_index':0}
errors = []
issue_links = []

def read_info():
    global info
    if os.path.exists(info_path):
        with open(info_path,'r') as f:
            info = json.load(f)
    

def write(htmls):
    if htmls == None or len(htmls) == 0:
        return None
    
    for h in htmls:
        if not os.path.exists(os.path.dirname(h.file_name)):
            os.makedirs(os.path.dirname(h.file_name))
        with open(h.file_name,'w') as f:
            print('file name:',h.file_name)
            print('link:',h.link,'id:',h.id)
            #print(h.__dict__)
            json.dump(h.__dict__,f)

    

def crawl(htmls):
    if htmls == None or len(htmls) == 0:
        return None
    
    for h in htmls:
        print('\t',h.link,end=' : ')
        res = requests.get(h.link,headers={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                          'referer': 'https://www.google.com/',
                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'})
        
        if res.status_code == 200:
            h.set_id(utils.get_id_form_link('https?://(.*)cnn.com/(.*)',h.link,2))
            h.set_time(find_time_from_link(h.link,res.text))
            h.set_file_name(utils.get_file_name_from_id(r'D:\Documents\code\predictor\cnn_news_data\html',h.time,h.id))
            h.set_html(str(res.content))
            print('success')
        else:
            raise RuntimeError('respone exception',h.link)
            issue_links.append(h.link)
            htmls.remove(h)
            print('fail')
            
        time.sleep(3.1 * random.random())
    return htmls

def find_time_from_link(link,text):
    '''
    if link == 'https://www.cnn.com/travel/article/lviv-ukraine-culture-capital/index.html':
        time = {'year':2012,'month':7,'day':12}
        return time
        '''
    parts = re.split('[/]',re.search('https?://(.*)cnn.com/(.*)',link).group(2))
    time_list = []
    time_dict = {}
    for p in parts:
        if re.match('\d+',p):
            time_list.append(p)
            
    if len(time_list) < 3:
        time_dict = find_time(text)
    else: 
        time_dict['year'] = time_list[0]
        time_dict['month'] = time_list[1]
        time_dict['day'] = time_list[2]
    return time_dict

def find_time(text):
    soup = BeautifulSoup(text,'html.parser')
    update_time = soup.find('p',class_='update-time')
    if update_time != None:
        time_list = re.split(' ',update_time.get_text())[-4:-1]
        
    else:
        update_time = soup.find('div',class_='Article__subtitle')
        time_list = re.split(' ',update_time.get_text())[-3:]
        time_list[0] = re.search('\d+',time_list[0]).group(0)
        temp = time_list[0]
        time_list[0] = time_list[1]
        time_list[1] = temp
        
    time_dict = {'year':time_list[2],'month':list(calendar.month_abbr).index(time_list[0][0:3]),'day':re.match('\d+',time_list[1])}
    return time_dict

def update(jump=False):
    if jump:
        info['month']+=1
        info['year'] += info['month'] // 12
        info['month'] = info['month'] % 12
        info['start_index'] = 0
    else:
        info['start_index'] += 10

def write_info():
    with open(info_path,'w') as f:
        json.dump(info,f)

def link_process(news):
    for n in news:
        if 'index.html' not in n.link:
            n.link = n.link + 'index.html'
        
    return news
if __name__ == '__main__':
    read_info()
    g_spider = gn_page('CNN','CNN',True)
    while(info['year'] <= 2020 or info['month'] <= 11):
        try:
            print(info)
            write_info()
            news = link_process(g_spider(info))
            '''
            if 'https://www.cnn.com/interactive/2018/12/asia/patrick-ho-ye-jianming-cefc-trial-intl/index.html' in news:
                news.remove('https://www.cnn.com/interactive/2018/12/asia/patrick-ho-ye-jianming-cefc-trial-intl/index.html')
                '''
            print(len(news))
            news = crawl(news)
            write(news)
            
            if news == None or len(news) == 0:
                update(True)
            else:
                update()
        
        except RuntimeError as e:
            if str(e.args[0]) == 'invalid time format' or str(e.args[0]) == 'respone exception':
                with open(r'D:\Documents\code\predictor\cnn_news_data\html\issue_links.txt','a') as f:
                    f.write('\n' + str(e.args[0]) + ' : ' + e.args[1]+'\n')
                    json.dump(info,f)
                    
            update()
        except requests.exceptions.ConnectTimeout as e:
            time.sleep(30)
        except Exception as e:
            raise

