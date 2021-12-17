import torch
import torch.nn as nn

from .helper_func import tensor_to_np


class Zeronet(nn.Module):
    def forward(self, x):
        """
        Return a zero-out copy of x
        :param x: torch.Tensor
        :return: x*0, type torch.Tensor
        """
        return torch.zeros_like(x)


class Parameter(nn.Module):
    def __init__(self, val, frozen=False):
        """
        A parameter that can be frozen to a hyper-parameter and defrost to a trainable parameter.
        :param val: initial value, type float / np.array / torch.Tensor
        :param frozen: whether the value starts out frozen, type bool, default to be trainable / not frozen
        """
        super().__init__()
        self.val = torch.Tensor(val)
        self.param = nn.Parameter(self.val)
        self.frozen = frozen

    def forward(self):
        """
        Access the value of parameter
        :return: parameter value, either torch.Tensor or nn.Parameter depending on whether it is frozen
        """
        if self.frozen:
            self.val = self.val.to(self.param.device)
            return self.val
        else:
            return self.param

    def freeze(self):
        self.val = self.param.detach().clone()
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def __repr__(self):
        return "val: {}, param: {}, frozen: {}".format(tensor_to_np(self.val), tensor_to_np(self.param), self.frozen)


class MLP(nn.Module):
    def __init__(self, *args, actv=nn.ReLU()):
        """
        Initialize a multiple layer perceptron network / simple multi-layer dense network
        :param args: list of layer size, starting from the input size and ending with output size, type uint
        :param actv: activation function, type nn.Module
        """
        super().__init__()
        self.linears = nn.ModuleList()
        for i in range(len(args)):
            self.linears.append(nn.Linear(args[i], args[i + 1]))
        self.actv = actv

    def forward(self, x):
        for i in range(self.layer_cnt):
            x = self.linears[i](x)
            if i < self.layer_cnt - 1:
                x = self.actv(x)
        return x

    @property
    def layer_cnt(self):
        return len(self.linears)
