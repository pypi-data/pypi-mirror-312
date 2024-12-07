import torch

from .loss_record import LossRecord, LossRecordGather
from src.lstm_dl_model.lstm.model import LstmModel
from src.lstm_dl_model.data import get_device


class LstmModelTrainer:
    def __init__(
            self,
            model: LstmModel,
            epochs: int,
            loss_func,
            optimizer,
            train_data_loader,
            test_data_loader
    ):
        self._model: LstmModel = model
        self._epochs: int = epochs
        self._loss_func = loss_func
        self._optimizer = optimizer
        self._train_data_loader = train_data_loader
        self._test_data_loader = test_data_loader

    def _train_one_epoch(self) -> LossRecord:
        self._model.train(mode=True)
        record: LossRecord = LossRecord()

        for batch_index, batch in enumerate(self._train_data_loader):
            x_batch, y_batch = batch[0].to(get_device()), batch[1].to(get_device())

            output = self._model.forward(x_batch)
            loss = self._loss_func(output[-1], y_batch)

            self._optimizer.zero_grad()
            loss.backward()
            self._optimizer.step()
            record.append_loss(loss)
        return record

    def _evaluate_one_epoch(self) -> LossRecord:
        self._model.eval()
        record: LossRecord = LossRecord()

        for batch_index, batch in enumerate(self._test_data_loader):
            x_batch, y_batch = batch[0].to(get_device()), batch[1].to(get_device())

            with torch.no_grad():
                output: torch.Tensor = self._model.forward(x_batch)
                loss = self._loss_func(output[-1], y_batch)
                record.append_loss(loss)
        return record

    def train(self, early_stopping_iter: int = 10) -> LossRecordGather:
        loss_record_gather = LossRecordGather()
        _early_stopping_counter: int = 0

        for epoch in range(self._epochs):
            _train_loss_record: LossRecord = self._train_one_epoch()
            _eval_loss_record: LossRecord = self._evaluate_one_epoch()
            loss_record_gather.append_loss_record(_eval_loss_record)

            print(f'EPOCH: {epoch}')
            print(f'TRAIN AVG LOSS: {_train_loss_record.average_loss} | LOWEST LOSS: {_train_loss_record.lowest_loss} | HIGHEST LOSS: {_train_loss_record.highest_loss}')
            print(f'EVALUATE AVG LOSS: {_eval_loss_record.average_loss} | LOWEST LOSS: {_eval_loss_record.lowest_loss} | HIGHEST LOSS: {_eval_loss_record.highest_loss}')
            print('-------------------------------------------------------------------------------------------------')

            if _early_stopping_counter:
                _early_stopping_counter += 1
                if _early_stopping_counter >= early_stopping_iter:
                    break

        return loss_record_gather
