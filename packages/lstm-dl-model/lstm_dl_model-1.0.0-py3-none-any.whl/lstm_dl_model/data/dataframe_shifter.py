from typing import Any
import numpy as np
from numpy import dtype, ndarray


class DataFrameShifter:
    def __init__(self, input_sequences, output_sequence, num_steps_backwards: int, num_steps_forwards: int):
        self._labels, self._targets = list(), list()  # instantiate labels and targets

        for i in range(len(input_sequences)):
            # find the end of the input, output sequence
            end_index: int = i + num_steps_backwards
            out_end_index: int = end_index + num_steps_forwards - 1
            # check if we are beyond the dataset
            if out_end_index > len(input_sequences):
                break
            # gather input and output of the pattern
            seq_x, seq_y = input_sequences[i:end_index], output_sequence[end_index - 1:out_end_index, -1]
            self._labels.append(seq_x), self._targets.append(seq_y)

    @property
    def labels_sequence(self) -> ndarray[Any, dtype]:
        return np.array(self._labels)

    @property
    def targets_sequence(self) -> ndarray[Any, dtype]:
        return np.array(self._targets)
