# tests/test_tensor_utils.py
import unittest
import torch
from torch_utils.tensor_utils import to_device


class TestTensorUtils(unittest.TestCase):
    def test_to_device(self):
        tensor = torch.tensor([1, 2, 3])
        self.assertEqual(to_device(tensor, 'cpu').device.type, 'cpu')
        if torch.cuda.is_available():
            self.assertEqual(to_device(tensor, 'cuda').device.type, 'cuda')


if __name__ == "__main__":
    unittest.main()
