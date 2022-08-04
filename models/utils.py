import numpy as np
from tensorflow.data import Dataset
from random import choice
from time import time

class DataProcessor():
    def __init__(self,data,batch_size):
        self.data = data
        self.batch_size = batch_size

    def sample(self):
        x = np.random.randint(self.data.shape[1],size=[self.batch_size],dtype='int16')

        yp = []
        yn = []
        for i in range(self.batch_size):
            yp.append(choice(np.arange(self.data.shape[0])[self.data[:,x[i]] == 1]))  
            yn.append(choice(np.arange(self.data.shape[0])[self.data[:,x[i]] == -1]))

        return x,np.concatenate([self.data[yp,x],self.data[yn,x]],axis=1)

    def toDataBatch(self,batchsz=8):
        x,y = self.sample()
        DataBatch = Dataset.from_tensor_slices((x,y))
        DataBatch = DataBatch.batch(batchsz)
        return DataBatch


if __name__ == '__main__':
    train_data = np.load(r'train_data.npy')
    t1 = time()
    train_dp = DataProcessor(train_data,128)
    train_db = train_dp.toDataBatch()
    print(time() - t1)
