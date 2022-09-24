import json
import os

if __name__ == '__main__':
    for year in os.listdir(r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data\html'):
        folder = r'C:\Users\Windows\Documents\GitHub\predictor\reuters_news_data\html' +'\\' + year
        for month in os.listdir(folder):
            for day in os.listdir(folder + '\\' + month):
                file = folder + '\\' + month + '\\' + day
                
                with open(file,'r') as f:
                    try:
                        data = json.loads(f.read())
                    except json.decoder.JSONDecodeError as e:
                        print(file)

                l = [i['link'] for i in data]
                s = set(l)
                
                if len(s) == len(l):
                    continue
                else:
                    print(file)
                    v = []
                    for link in s:
                        v.append(l.index(link))
                    r = set(range(len(l))) - set(v)
                    for i in r:
                        data[i] = None
                    for i in range(len(r)):
                        data.remove(None)
                        
                    with open(file,'w') as f:
                        f.write(json.dumps(data))

