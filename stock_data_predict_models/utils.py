import numpy as np
import pandas as pd
import tensorflow as tf
import random

class DataProcessor():
    def __init__(self,data,batch_size):
        self.data = data
        self.batch_size = batch_size

    def sample(self):
        x = np.random.randint(self.data.shape[1],size=[self.batch_size],dtype='int16')
        pos = []
        neg = []
        for i in x:
            pos.append(self.data[self.data[:,i] == 1])
            neg.append(self.data[self.data[:,i] == -1])
            pos[-1] = pos[-1][random.randint(0,(pos[-1].shape[0]-1))]
            neg[-1] = neg[-1][random.randint(0,(neg[-1].shape[0]-1))]
        pos = np.array(pos)
        neg = np.array(neg)
        return x,np.concatenate([pos,neg],axis=1)

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = tf.data.Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch

if __name__ == '__main__':
    train_data = np.load(r'train_data.npy')
    test_data = np.load(r'test_data.npy')
    print('read')
    train_dp = DataProcessor(train_data,4)
    test_dp = DataProcessor(test_data,4)
    print('processed')
    train_db = train_dp.toDataBatch()
    test_db = test_dp.toDataBatch()
    sample = next(iter(train_db))
    print('batch:', sample)
    
