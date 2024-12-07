import numpy as np
from torch import Tensor
from torch.utils.data import Dataset


class DataBatch:
    def __init__(self, data: dict) -> None:
        self.Data: dict[str, float] = data
        self.OutputData: float = self.Data.pop('close')
        self.InputData: list[float] = list(self.Data.values())
    
    @property
    def OUTPUT_DATA(self):
        return np.array(self.OutputData)
    
    @property
    def INPUT_DATA(self):
        return np.array(self.InputData)


class Sequence:
    def __init__(self, input_sequences, output_sequence) -> None:
        self.InputSequnece = input_sequences
        self.OutputSequence = output_sequence
    
    def __len__(self):
        total_len = len(self.InputSequnece) + len(self.OutputSequence) - 1
        return total_len
    
    @property
    def INPUT_SEQUENCE(self):
        return self.InputSequnece

    @property
    def OUTPUT_SEQUENCE(self):
        return self.OutputSequence


class MlStockDataSet(Dataset):
    def __init__(self, x: Tensor, y: Tensor) -> None:
        super().__init__()
        self.X = x
        self.Y = y

    def __len__(self) -> int:
        return len(self.X)
    
    def __getitem__(self, index) -> tuple[Tensor, Tensor]:
        return self.X[index], self.Y[index]
