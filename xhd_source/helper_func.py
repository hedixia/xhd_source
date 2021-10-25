import pathlib


def tensor_to_np(x):
    """
    Cast a tensor to numpy
    :param x: type torch.Tensor
    :return x: type np.array
    """
    for method in ['detach', 'cpu', 'numpy']:
        if hasattr(x, method):
            x = getattr(x, method)()
    return x


def count_parameters(model):
    """
    Compute the number of trainable parameters of the model.
    :param model: type nn.Module
    :return: number of parameters, type int
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def shrink_parameters(model, ratio):
    """
    Shrink all parameters of a model to a certain ratio
    :param model: type nn.Module
    :param ratio: type float
    :return:
    """
    model_dict = model.state_dict()
    for i in model_dict:
        model_dict[i] *= ratio
    model.load_state_dict(model_dict)
    return model


def mkdir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
