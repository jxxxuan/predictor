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
sys.path.append(r'D:\Documents\predictor\news')
from news_processor import utils
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

class Albert_Trainer():
    def __init__(self,vocab_file=None,file_path=None,max_length=128,batchsz=1,batch=1,b=0.15):
        self.data = self.load_data(file_path)
        self.num_prg = len(self.data)
        self.batchsz = batchsz
        self.batch = batch
        self.vocab = self.load_vocab_file(vocab_file)
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.max_length = max_length
        self.b = b

    def load_data(self,file_path):
        
        with open(file_path,'r') as reader:
            data = json.loads(reader.read())
        return data

    def load_vocab_file(self,vocab_file):
        vocab = pd.read_csv(vocab_file,index_col=0)
        return vocab[vocab['en_Trainable']]['en_ids1'].to_dict()

    def convert_ids_to_tokens(self,ids):
        output = []
        for item in ids:
            output.append(self.inv_vocab[item])
        return output

    def choice(self):
        paragraphs = np.random.choice(self.data,self.batchsz)
        
        data = np.zeros((self.batchsz,self.max_length),dtype='int16')
        mask = np.zeros((self.batchsz,self.max_length),dtype='int16')
        types = np.zeros((self.batchsz,self.max_length),dtype='int16')
        output = np.zeros((self.batchsz,self.max_length),dtype='int16')
        for i in range(self.batchsz):
            paragraphs[i] = paragraphs[i][:self.max_length]
            output[i,:len(paragraphs[i])] = paragraphs[i]
            data[i,:len(paragraphs[i])] = paragraphs[i]
            mask[i,:len(paragraphs[i])] = 1
            '''
            temp = np.full((len(paragraphs[i])),False)
            temp[:self.max_length] = True
            
            skip = False
            for t in range(len(paragraphs[i])):
                if random.choices([False,True],weights=[1-self.b*1/2,self.b*1/2])[0] and paragraphs[i][t] == 48:
                    paragraphs[i][t] = 29
                    skip = True
                elif skip:
                    temp[t] = False
                    if paragraphs[i][t] == 49:
                        skip = False
            data[i,:len(temp[temp])] = np.array(paragraphs[i])[temp]
            mask[i,:len(temp[temp])] = 1
            '''
            
        data[np.random.choice([False,True],size=data.shape,p=[1-self.b,self.b])] = 29
        return data,mask,types,output

    def __call__(self):
        t1 = time()
        encoder_inputs = self.choice()
        print("Generate data -",time() - t1)
        return tf.data.Dataset.from_tensor_slices((encoder_inputs[:3],tf.one_hot(encoder_inputs[-1],depth=len(self.vocab),dtype="int8"))).batch(self.batch)
    
if __name__ == '__main__':
    test_file = r'C:\Users\User\Documents\predictor\data\reuters_news\test.txt'
    vocab_file = r'C:\Users\User\Documents\predictor\data\vocab.csv'
    pre = Albert_Trainer(vocab_file,test_file,batchsz=1,batch=1)
    print(next(iter(pre())))
