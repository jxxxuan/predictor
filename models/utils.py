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

    def sample(self):
        x = np.random.randint(self.data.shape[1],size=[self.batch_size],dtype='int16')

        yp = []
        yn = []
        for i in range(self.batch_size):
            yp.append(random.choice(np.arange(self.data.shape[0])[self.data[:,x[i]] == 1], size=[self.avr]))  
            yn.append(random.choice(np.arange(self.data.shape[0])[self.data[:,x[i]] == -1], size=[self.avr]))

        y = np.concatenate([self.data[yp],self.data[yn]],axis=2)
        y = np.mean(y,axis=1)
        return x,y

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

class LabelProcessor():
    def __init__(self,data,batch_size):
        self.data = data
        self.batch_size = batch_size
        self.length = len(set(self.data))

    def sample(self):
        s = self.data.sample(self.batch_size)
        print(s)
        return s.index.values,s.values

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        y = tf.one_hot(y, depth=self.length)
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

if __name__ == '__main__':
    train_data = pd.read_pickle(r'label_data/974_test.pkl')['label']
    t1 = time()
    train_dp = LabelProcessor(train_data,128)
    train_db = train_dp.toDataBatch()
    print(time() - t1)
