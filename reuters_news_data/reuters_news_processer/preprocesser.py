import json
import os
from bs4 import BeautifulSoup
import utils
import numpy as np

def info_filter():
    files = utils.get_reuters_news('html')
    for file in files:
        with open(file['file_name'],'r') as f:
            data = json.loads(f.read())
        news = []

        for info in data:
            soup = BeautifulSoup(info['html'],'html.parser')
            link = info['link']
            
            title = soup.findAll('h1',class_='Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj')
            if len(title) == 0:
                title = soup.findAll('h1',class_='Headline-headline-2FXIq Headline-white-16WmR SponsoredArticleHeader-headline-1Rkqd')
            if len(title) == 0:
                title = soup.findAll('h1',class_='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_2__1K_hh heading__base__2T28j heading__heading_2__3Fcw5')
            
            paragraph = soup.findAll('p',class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
            if len(paragraph) == 0:
                paragraph = soup.findAll('p',class_='text__text__1FZLe text__dark-grey__3Ml43 text__regular__2N1Xr text__large__nEccO body__base__22dCE body__large_body__FV5_X article-body__element__2p5pI')
            if len(paragraph) == 0:
                paragraph = [i.findChild() for i in soup.findAll('div',class_='ArticleBody-p-table-3vPxs')]

            if len(paragraph) == 0 or len(title) == 0:
                '''
                print('content:',len(paragraph))
                print('title:',len(title))
                print(link)
                '''
            else:
                title = title[0].text
                content = []
                for p in paragraph:
                    content.append(p.text)
                news.append({'link':link,'title':title,'content':content})

        folder_name = r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data\data' + '\\' + file['file_name'][-14:-6]
        file_name = folder_name + '\\' + file['file_name'][-6:]
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            
        with open(file_name,'w') as f:
            f.write(json.dumps(news))
            
if __name__ == '__main__':
    info_filter()
        
