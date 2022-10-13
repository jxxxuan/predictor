import numpy as np
import pandas as pd
import tensorflow as tf
import json
from tensorflow.data import Dataset
import random
from numpy import random as nrandom
from time import time
'''
import sys
sys.path.append(r'D:\Documents\predictor\reuters_news')
from reuters_news_processer import utils
'''

class Cdata6808Processor():
    def __init__(self,data,batch_size,avr=1):
        self.data = data
        self.batch_size = batch_size
        self.avr= avr
        self.range = np.arange(self.data.shape[0])

    def sample(self):
        x = np.nrandom.randint(self.data.shape[1],size=[self.batch_size],dtype='int16')

        yp = []
        yn = []
        for i in range(self.batch_size):
            yp.append(nrandom.choice(self.range[self.data[:,x[i]] == 1], size=[self.avr]))  
            yn.append(nrandom.choice(self.range[self.data[:,x[i]] == -1], size=[self.avr]))

        y = np.concatenate([self.data[yp],self.data[yn]],axis=2)
        y = np.mean(y,axis=1)
        return x,y

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

class Cdata3404Processor():
    def __init__(self,data,batch_size=8,input_size=100):
        self.data = data
        self.batch_size = batch_size
        self.input_size= input_size
        self.b = self.data != 0
        self.range = np.arange(self.data.shape[1])

    def sample(self):
        yp = nrandom.randint(self.data.shape[0],size=[self.batch_size],dtype='int16')
        x = np.zeros([self.batch_size,2,self.input_size],dtype='int8')
        
        for i in range(self.batch_size):
            x[i,0] = nrandom.choice(self.range[self.b[yp[i]]],size=self.input_size)
            x[i,1] = self.data[yp[i],x[i,0]]

        return x,self.data[yp]
    
    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch
        
class LabelProcessor():
    def __init__(self,data,name_list,batch_size):
        self.data = data
        self.batch_size = batch_size
        self.name_list = name_list
        self.length = len(set(self.name_list))

    def sample(self):
        s = self.name_list.sample(self.batch_size)
        return self.data[s.index,:],s.values

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        y = tf.one_hot(y, depth=self.length)
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

    
class albert_en_preprocess():
  def __init__(self,vocab_file,ids_input=False,len_sequence=128):
    self.ids_input = ids_input
    if not self.ids_input:
      self.vocab = load_vocab(vocab_file)
    self.full_tokenizer = FullTokenizer(self.vocab)
    self.len_sequence = len_sequence
    
  def __call__(self,text,ids,mask=False):
    input_mask = np.zeros(self.len_sequence,dtype='int8')
    input_type_ids = np.zeros(self.len_sequence,dtype='int8')
    if self.ids_input:
      input_word_ids = self.ids
    else:
      tokens = self.full_tokenizer.tokenize(text)
      input_word_ids = self.convert_tokens_to_ids(tokens)
      if mask:
        r = np.random.randint(2,size=input_word_ids.size)
        input_mask[:r.size] = r
      else:
        input_mask[:len(tokens)+2] = 1

    return {'input_word_ids':input_word_ids,'input_mask':input_mask,'input_type_ids':input_type_ids}

  def convert_tokens_to_ids(self, tokens):
    output = np.zeros(self.len_sequence,dtype='int32')
    ids = self.full_tokenizer.convert_tokens_to_ids(tokens)
    output[:len(ids)] = ids
    return output

class NewsProcessor():
    def __init__(self,vocab_file=None,file_path=None,mask=False,batchsz=32):
        self.data = self.load_data(file_path)
        self.num_prg = len(self.data)
        self.batchsz = batchsz
        self.vocab = self.load_vocab_file(vocab_file)
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.mask = mask

    def load_data(self,file_path):
        
        with open(file_path,'r') as reader:
            data = json.loads(reader.read())
        '''
        files = utils.get_reuters_news(r'D:\Documents\predictor\data\reuters_news\ids_data')
        data = []
        for file in files[:10]:
            with open(file['file_name'],'r') as reader:
                text = json.loads(reader.read())
            for news in text:
                for p in news['content']:
                    data.append(tuple(p))
        '''
        return data

    def load_vocab_file(self,vocab_file):
        vocab = pd.read_csv(vocab_file,index_col=0)
        return vocab[vocab['en']]['ids1'].to_dict()

    def convert_ids_to_tokens(self,ids):
        output = []
        for item in ids:
            output.append(self.inv_vocab[item])
        return output

    def choice(self,b=0.1):
        paragraphs = []
        for i in range(self.batchsz):
            paragraphs.append(self.data[random.randint(0,self.num_prg)])
        
        data = np.zeros((self.batchsz,max([len(p) for p in paragraphs])),dtype='uint32')
        mask = np.zeros((self.batchsz,max([len(p) for p in paragraphs])),dtype='uint32')
        for i in range(len(paragraphs)):
            data[i,:len(paragraphs[i])] = paragraphs[i]
            mask[i,:len(paragraphs[i])] = np.ones(len(paragraphs[i]))
            '''
            if self.masking:
                mask[i,:len(paragraphs[i])] = nrandom.choice((0,1),[len(paragraphs[i])],p=[b,1-b])
            else:
                mask[i,:len(paragraphs[i])] = np.ones(len(paragraphs[i]))
            '''
        return data,mask

    def __call__(self):
        inputs = dict()
        inputs['input_word_ids'],inputs['input_mask'] = self.choice()
        encoder_inputs = dict(
            input_word_ids=tf.convert_to_tensor(inputs['input_word_ids'],dtype='int32',name='input_word_ids'),
            input_mask=tf.convert_to_tensor(inputs['input_mask'],dtype='int32',name='input_mask'),
            input_type_ids=tf.convert_to_tensor(np.zeros_like(inputs['input_word_ids']),dtype='int32',name='input_type_ids'),
        )
        return Dataset.from_tensor_slices((encoder_inputs,tf.one_hot(encoder_inputs['input_word_ids'],depth=len(self.vocab)))).batch(4)
    
if __name__ == '__main__':
    fine_tune = r'D:\Documents\predictor\reuters_news\fine_tune.txt'
    vocab_file = r'D:\Documents\predictor\reuters_news\reuters_news_processer\vocab.csv'
    pre = NewsProcessor(vocab_file=vocab_file)
    #pre = NewsProcessor(vocab_file,fine_tune)
    t1 = time()
    print(next(iter(pre())))
    print(time() - t1)
