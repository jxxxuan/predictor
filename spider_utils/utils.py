import re

trans = str.maketrans('/\\|:*><?"-','-_________')

class Html():
    
    def __init__(self,link):
        self.link = link
    def set_html(self,html):
        self.html = html
    def set_file_name(self,file_name):
        self.file_name = file_name
    def set_id(self,id_):
        self.id = id_
    def set_time(self,time):
        self.time = time

class News():
    def __init__(self,file_name=None,link=None,time=None,title=None,content=None,id_=None,class_=None):
        self.link = link
        self.time = time
        self.title = title
        self.content = content
        self.class_ = class_
        self.id = id_
        self.file_name = file_name
        
    def set_link(self,link):
        self.link = link
    def set_time(self,time):
        self.time = time
    def set_title(self,title):
        self.title = title
    def set_content(self,content):
        self.content = content
    def set_class(self,class_):
        self.class_ = class_
    def set_file_name(self,file_name):
        self.file_name = file_name
    def set_id(self,id_):
        self.id = id_

def get_file_name_from_id(path,time,file_id):
    return path + '\\' + str(time['year']) + '\\' + str(time['month']) + '\\' + file_id + '.json'

def get_id_form_link(t,link,grp):
    return re.split('[?]',re.search(t,link).group(grp))[0].translate(trans)
