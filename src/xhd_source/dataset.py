import os

import numpy as np
import torch

from .helper_func import tensor_to_np


class Dataset:
    def __init__(self, path):
        self.path = path
        self.data = dict()
        self.files = set(os.listdir(path))

    def __getattr__(self, item):
        xname = item + "_x"
        yname = item + "_y"
        x = self.__get_helper(xname)
        y = self.__get_helper(yname)
        return x, y

    def __get_helper(self, fname, type='np', device='cpu'):
        if fname not in self.data:
            if fname + '.npy' in self.files:
                self.data[fname] = np.load(fname)
            elif fname + '.csv' in self.files:
                self.data[fname] = np.loadtxt(fname, delimiter=',')
        if type == 'torch':
            self.data[fname] = torch.Tensor(self.data[fname])
        if device != 'cpu':
            self.data[fname] = self.data[fname].to(device)
        return self.data[fname]

    def save(self, path=None, verbose=False):
        path = self.path if path is None else path
        for fname in self.data:
            file_path = os.path.join(path, fname + '.npy')
            odata = tensor_to_np(self.data[fname])
            np.save(file_path, odata)
            if verbose:
                print('File {} saved with shape {}.'.format(fname, odata.shape))
