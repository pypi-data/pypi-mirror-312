# torch_utils/tensor_utils.py
import torch


def to_device(tensor, device='cpu'):
    """
    將 Tensor 移動到指定設備（CPU 或 GPU）。
    Args:
        tensor (torch.Tensor): 要移動的張量。
        device (str): 設備名稱（如 'cpu', 'cuda'）。
    Returns:
        torch.Tensor: 移動後的張量。
    """
    if not torch.is_tensor(tensor):
        raise ValueError("Input must be a torch.Tensor")
    return tensor.to(device)
