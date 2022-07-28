import numpy as np
import pandas as pd
import tensorflow as tf
import random

class DataProcessor():
    def __init__(self,data,batch_size):
        self.data = data
        self.batch_size = batch_size

    def sample(self):
        x = np.random.randint(self.data.shape[1],size=[self.batch_size])
        pos = []
        neg = []
        for i in x:
            pos.append(self.data[self.data[:,i] == 1])
            neg.append(self.data[self.data[:,i] == -1])
            pos[-1] = pos[-1][random.randint(0,pos[-1].shape[0])]
            neg[-1] = neg[-1][random.randint(0,neg[-1].shape[0])]
        pos = np.array(pos)
        neg = np.array(neg)
        return x,np.concatenate([pos,neg],axis=1)

    def toDataBatch(self):
        x,y = self.sample()
        train_db = tf.data.Dataset.from_tensor_slices((x,y))
        train_db = train_db.batch(8)
        return DataBatch

if __name__ == '__main__':
    d = np.load(r'train_data.npy')
    dp = DataProcessor(d,16)
    x,y = dp.sample()
    
