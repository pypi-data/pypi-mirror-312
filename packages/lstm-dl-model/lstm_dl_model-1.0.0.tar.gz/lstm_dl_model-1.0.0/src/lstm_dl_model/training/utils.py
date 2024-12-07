from torch import Tensor
import torch.nn as nn
import numpy as np
import torch


def get_loss_function(loss_func) -> float:
    def loss_function(inputs, targets):
        mse_loss: float = loss_func()(inputs, targets)
        return mse_loss
    return loss_function


def get_optimizer(optim, model_parameters, learning_rate: float):
    optimizer = optim(params=model_parameters, lr=learning_rate)
    return optimizer
