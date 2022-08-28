import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import time
import re
import calendar

class gn_engine():
    def __init__(self,name=None,key_word=None,start_time=datetime(2003,11,1)):
        self.name = name
        self.key_word = key_word
        self.time = start_time
        self.delta = timedelta(days=1)
        self.index = 0
        self.google_link = ''

    def set_info(self,res):
        soup = BeautifulSoup(res.content,'html.parser')
        a = soup.find_all('a',class_='WlydOe')
        news_links = []
        news_info = {}
        for i in a:
            if i.find('div',class_='CEMjEf NUnG9d').find('span').get_text() in self.name:
                news_info['link'] = i['href']
                news_info['time'] = self.format_time(i.find('div',class_='OSrXXb ZE0LJd').find('span').get_text())
                news_info['google_link'] = self.google_link
                news_links.append(news_info.copy())
        if len(news_links) == 0:
            time.sleep(3)
        return news_links
    
    def __iter__(self):
        return self

    def __next__(self):
        self.google_link =  'https://www.google.com/search?q='+self.key_word+'&newwindow=1&tbs=cdr:1,cd_min:'+self.time.strftime('%m-%d-%Y') + ',cd_max:'+(self.time+self.delta).strftime('%m-%d-%Y')+'&tbm=nws&sxsrf=ALiCzsa8NRiPOkqTIdYfSU2qjW_qqM9cFA:1652446506081&ei=KlV-YuaoBNKzmgesmIuABA&start='+str(self.index)+'&sa=N&ved=2'
        print(self.google_link)
        res = requests.get(self.google_link,headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'})
        links = self.set_info(res)
        if len(links) == 0:
            self.time += self.delta
            self.index = 0
            return self.__next__()
        else:
            self.index += 10
        return links

    def get_index(self):
        return {'year':self.time.year,'month':self.time.month,'day':self.time.day,'index':self.index}
    
    def format_time(self,time):
        time_list = re.split(' ',time)
        time = datetime(day=int(time_list[0]),month=list(calendar.month_abbr).index(time_list[1][0:3]),year=int(time_list[2]))
        return time

'''
if __name__ == '__main__':
    gn = gn_engine('CNN','CNN')
    gn = iter(gn)
    for i in range(1):
        print(next(gn))
'''
