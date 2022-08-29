import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.data import Dataset
from numpy import random
from time import time

class Cdata6808Processor():
    def __init__(self,data,batch_size,avr=1):
        self.data = data
        self.batch_size = batch_size
        self.avr= avr
        self.range = np.arange(self.data.shape[0])

    def sample(self):
        x = np.random.randint(self.data.shape[1],size=[self.batch_size],dtype='int16')

        yp = []
        yn = []
        for i in range(self.batch_size):
            yp.append(random.choice(self.range[self.data[:,x[i]] == 1], size=[self.avr]))  
            yn.append(random.choice(self.range[self.data[:,x[i]] == -1], size=[self.avr]))

        y = np.concatenate([self.data[yp],self.data[yn]],axis=2)
        y = np.mean(y,axis=1)
        return x,y

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

class Cdata3404Processor():
    def __init__(self,data,batch_size,input_size=100):
        self.data = data
        self.batch_size = batch_size
        self.input_size= input_size
        self.b = self.data != 0
        self.range = np.arange(self.data.shape[1])

    def sample(self):
        yp = random.randint(self.data.shape[0],size=[self.batch_size],dtype='int16')
        x = np.zeros([self.batch_size,2,self.input_size],dtype='int16')
        
        for i in range(self.batch_size):
            x[i,0] = random.choice(self.range[self.b[yp[i]]],size=self.input_size)
            x[i,1] = self.data[yp[i]][(x[i,0])]
        print(x.shape)
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

if __name__ == '__main__':
    
    data = np.load(r'C:\Users\Windows\Documents\GitHub\predictor\models\int_data\9172_test.npy')
    t1 = time()
    train_dp = Cdata3404Processor(data,512)
    train_db = train_dp.toDataBatch()
    print(time() - t1)
