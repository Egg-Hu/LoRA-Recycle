import torch
import numpy as np


class CategoriesSampler():

    def __init__(self, label, n_batch, n_cls, n_per):
        self.n_batch = n_batch
        self.n_cls = n_cls
        self.n_per = n_per

        label = np.array(label)
        self.m_ind = []
        for i in range(min(label),max(label) + 1):
            ind = np.argwhere(label == i).reshape(-1)
            ind = torch.from_numpy(ind)
            self.m_ind.append(ind)#[[],[],...]


    def __len__(self):
        return self.n_batch

    def __iter__(self):
        for i_batch in range(self.n_batch):
            batch = []
            classes = torch.randperm(len(self.m_ind))[:self.n_cls]
            for c in classes:
                l = self.m_ind[c]
                pos = torch.randperm(len(l))[:self.n_per]
                batch.append(l[pos])#[[],[],...]
            batch = torch.stack(batch).t().reshape(-1)
            yield batch
class CategoriesSampler_star():

    def __init__(self, label, n_batch, n_cls, n_per):
        self.n_batch = n_batch
        self.n_cls = n_cls
        self.n_per = n_per

        label = np.array(label)
        self.m_ind = []
        for i in range(max(label) + 1):
            ind = np.argwhere(label == i).reshape(-1)[:self.n_per]##########
            ind = torch.from_numpy(ind)
            self.m_ind.append(ind)#[[],[],...]

    def __len__(self):
        return self.n_batch

    def __iter__(self):
        for i_batch in range(self.n_batch):
            batch = []
            classes = torch.randperm(len(self.m_ind))[:self.n_cls]
            for c in classes:
                l = self.m_ind[c]
                pos = torch.randperm(len(l))[:self.n_per]
                batch.append(l[pos])#[[],[],...]
            batch = torch.stack(batch).t().reshape(-1)
            yield batch
#select form specific classes
class CategoriesSampler_Specific():

    def __init__(self, label, n_batch, n_per,specific):
        self.n_batch = n_batch
        self.n_per = n_per
        self.specific=specific

        label = np.array(label)
        self.m_ind =dict()
        for i in specific:
            ind = np.argwhere(label == i).reshape(-1)
            ind = torch.from_numpy(ind)
            self.m_ind[i]=ind#[[],[],...]

    def __len__(self):
        return self.n_batch

    def __iter__(self):
        for i_batch in range(self.n_batch):
            batch = []
            for c in self.specific:
                l = self.m_ind[c]
                pos = torch.randperm(len(l))[:self.n_per]
                batch.append(l[pos])#[[],[],...]
            batch = torch.stack(batch).t().reshape(-1)
            yield batch


class RandomSampler():

    def __init__(self, label, n_batch, n_per):
        self.n_batch = n_batch
        self.n_per = n_per
        self.label = np.array(label)
        self.num_label = self.label.shape[0]

    def __len__(self):
        return self.n_batch

    def __iter__(self):
        for i_batch in range(self.n_batch):
            batch = torch.randperm(self.num_label)[:self.n_per]
            yield batch
            
            
# sample for each class
class ClassSampler():

    def __init__(self, label, n_per=None):
        self.n_per = n_per
        label = np.array(label)
        self.m_ind = []
        for i in range(max(label) + 1):
            ind = np.argwhere(label == i).reshape(-1)
            ind = torch.from_numpy(ind)
            self.m_ind.append(ind)

    def __len__(self):
        return len(self.m_ind)

    def __iter__(self):
        classes = torch.arange(len(self.m_ind))
        for c in classes:
            l = self.m_ind[int(c)]
            if self.n_per is None:
                pos = torch.randperm(len(l))
            else:
                pos = torch.randperm(len(l))[:self.n_per]
            yield l[pos]
            
            
# for ResNet Fine-Tune, which output the same index of task examples several times
class InSetSampler():

    def __init__(self, n_batch, n_sbatch, pool): # pool is a tensor
        self.n_batch = n_batch
        self.n_sbatch = n_sbatch
        self.pool = pool
        self.pool_size = pool.shape[0]

    def __len__(self):
        return self.n_batch

    def __iter__(self):
        for i_batch in range(self.n_batch):
            batch = self.pool[torch.randperm(self.pool_size)[:self.n_sbatch]]
            yield batch