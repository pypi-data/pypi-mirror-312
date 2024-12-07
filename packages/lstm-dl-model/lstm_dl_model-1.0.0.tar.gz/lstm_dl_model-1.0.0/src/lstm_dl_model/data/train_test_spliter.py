from torch import tensor, Tensor
from numpy import ndarray
import torch


class TrainTestSpliter:
    def __init__(self, labels: ndarray, targets: ndarray):
        _total_samples: int = len(labels)
        _train_test_cutoff: int = round(0.90 * _total_samples)

        _train_labels: Tensor = Tensor(labels[:_train_test_cutoff]).float()
        _test_labels: Tensor = Tensor(labels[_train_test_cutoff:]).float()

        _train_targets: Tensor = Tensor(targets[:_train_test_cutoff]).float()
        _test_targets: Tensor = Tensor(targets[_train_test_cutoff:]).float()

        _labels_train_reshaped_tensors: Tensor = torch.reshape(
            _train_labels,
            (
                _train_labels.shape[0],
                _train_labels.shape[1],
                _train_labels.shape[2]
            )
        )
        _labels_test_reshaped_tensors: Tensor = torch.reshape(
            _test_labels,
            (
                _test_labels.shape[0],
                _test_labels.shape[1],
                _test_labels.shape[2]
            )
        )

        self.splits_dict: dict[str, dict[str, tensor] | dict[str, tensor]] = {
            'labels': {
                'train': _labels_train_reshaped_tensors,
                'test': _labels_test_reshaped_tensors
            },
            'targets': {
                'train': _train_targets,
                'test': _test_targets
            }
        }

    @property
    def train_labels(self) -> Tensor:
        return self.splits_dict['labels']['train']

    @property
    def test_labels(self) -> Tensor:
        return self.splits_dict['labels']['test']

    @property
    def train_targets(self) -> Tensor:
        return self.splits_dict['targets']['train']

    @property
    def test_targets(self) -> Tensor:
        return self.splits_dict['targets']['test']
