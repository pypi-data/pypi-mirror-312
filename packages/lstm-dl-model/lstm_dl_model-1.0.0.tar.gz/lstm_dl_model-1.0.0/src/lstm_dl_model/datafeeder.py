from torch import Tensor
from torch.utils.data import DataLoader
import numpy as np
from sideclasses import *


class SequenceGenerator:
    def __init__(self, backward_sequence_len: int, forward_sequence_len: int) -> None:
        self.backward_sequence_len: int = backward_sequence_len
        self.forward_sequence_len: int = forward_sequence_len
        self.DataBatchDB: list[DataBatch] = list()
    
    def Update(self, data: DataBatch) -> None:
        self.DataBatchDB.append(data)
        data_batch_data_base_len = len(self.DataBatchDB)
        output_index = total_sequence_len = self.backward_sequence_len + self.forward_sequence_len - 1
        if data_batch_data_base_len > total_sequence_len:
            self.DataBatchDB = self.DataBatchDB[-output_index:]
        
    def GetSequence(self) -> (Sequence | None):
        data_batch_data_base_len = len(self.DataBatchDB)
        input_index = self.backward_sequence_len
        total_sequence_len = self.backward_sequence_len + self.forward_sequence_len - 1
        
        if data_batch_data_base_len == total_sequence_len:
            input_sequence = np.array([db.INPUT_DATA for db in self.DataBatchDB[0:input_index]])
            output_sequence = np.array([db.OUTPUT_DATA for db in self.DataBatchDB[input_index-1:]])
            sequence: Sequence = Sequence(input_sequences=input_sequence, output_sequence=output_sequence)
            return sequence

        elif data_batch_data_base_len < (total_sequence_len):
            return None
    
    def GetLastInputSequence(self) -> (Sequence | None):
        data_batch_data_base_len = len(self.DataBatchDB)
        input_index = self.backward_sequence_len
        total_sequence_len = self.backward_sequence_len + self.forward_sequence_len - 1

        if data_batch_data_base_len == (total_sequence_len):
            last_input_sequence = Sequence(
                input_sequences=np.array([db.INPUT_DATA for db in self.DataBatchDB[-input_index:]]),
                output_sequence=0.0
                )
            return last_input_sequence
        
        elif data_batch_data_base_len < (total_sequence_len):
            return None
        
    @property
    def IsSequenceAvilable(self) -> bool:
        sequence = self.GetSequence()
        if sequence is not None: return True
        else: return False


class DataFeederModel:
    def __init__(self, backward_sequence_len: int, forward_sequence_len: int) -> None:
        self.backward_sequence_len: int = backward_sequence_len
        self.forward_sequence_len: int = forward_sequence_len
        self.sequence_history_length: int = backward_sequence_len + forward_sequence_len
        self.SequenceGenerator: SequenceGenerator = SequenceGenerator(backward_sequence_len, forward_sequence_len)
        self.SequenceDB: list[Sequence] = list()
    
    def Update(self, data: DataBatch):
        # Update the Sequence Data Base:
        self.SequenceGenerator.Update(data=data)
        is_sequence_avilable = self.SequenceGenerator.IsSequenceAvilable
        sequence = self.SequenceGenerator.GetSequence()
        
        if is_sequence_avilable:
            self.SequenceDB.append(sequence)

        # Sequence Data Base length Checking:
        sequence_db_len = len(self.SequenceDB)
        if sequence_db_len > self.sequence_history_length:
            self.SequenceDB = self.SequenceDB[-self.sequence_history_length:]

    def DataLoaders(self) -> tuple[DataLoader, DataLoader]:
        train_seq, test_seq = self.SequenceDB[:-self.forward_sequence_len], self.SequenceDB[-self.forward_sequence_len:]

        x_train = Tensor(np.array([ts.INPUT_SEQUENCE for ts in train_seq]))
        y_train = Tensor(np.array([ts.OUTPUT_SEQUENCE for ts in train_seq]))
        x_test = Tensor(np.array([ts.INPUT_SEQUENCE for ts in test_seq]))
        y_test = Tensor(np.array([ts.OUTPUT_SEQUENCE for ts in test_seq]))

        train_data_set = MlStockDataSet(x_train, y_train)
        test_data_set = MlStockDataSet(x_test, y_test)
        train_data_loader = DataLoader(train_data_set, batch_size=1, shuffle=True)
        test_data_loader = DataLoader(test_data_set, batch_size=1)

        return train_data_loader, test_data_loader

    @property
    def IS_ENGINE_READY(self):
        sequence_db_len = len(self.SequenceDB)
        if sequence_db_len >= self.sequence_history_length: return True
        else: return False
    
    @property
    def LAST_INPUT_TENSOR(self) -> Tensor:
        last_input_sequence = self.SequenceGenerator.GetLastInputSequence()
        last_input_sequence_tensor: Tensor = Tensor(np.array(last_input_sequence.INPUT_SEQUENCE)).unsqueeze(0)
        return last_input_sequence_tensor
