import torch
from torch import Tensor
import torch.nn as nn
import numpy as np
from torch.optim import SGD


class LstmModel(nn.Module):
    def __init__(self, num_classes_output, input_size, hidden_size, num_layers, num_linear_connections,
                 dropout: float) -> None:
        super().__init__()
        self.num_classes = num_classes_output  # output size
        self.num_layers = num_layers  # number of recurrent layers in the lstm
        self.input_size = input_size  # input size
        self.hidden_size = hidden_size  # neurons in each lstm layer

        # LSTM model
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True,
                            dropout=dropout)  # lstm
        self.linear_func_1 = nn.Linear(hidden_size, num_linear_connections)  # fully connected
        self.linear_func_2 = nn.Linear(num_linear_connections, num_classes_output)  # fully connected last layer
        self.relu = nn.ReLU()

    def forward(self, x):
        # hidden state
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        # cell state
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)

        # propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0))  # (input, hidden, and internal state)
        out = self.relu(hn)
        out = self.linear_func_1(out)  # first dense
        out = self.relu(out)  # relu
        out = self.linear_func_2(out)  # final output
        return out


class LongShortTermMemoryEngineModel(LstmModel):
    def __init__(self, epochs: int, num_classes_output: int, input_size: int, hidden_size: int, num_layers: int,
                 num_linear_connections: int, dropout: float, learning_rate: float, train_data_loader,
                 test_data_loader) -> None:
        super().__init__(num_classes_output, input_size, hidden_size, num_layers, num_linear_connections, dropout)
        self.Optimiser = SGD(params=self.parameters(), lr=learning_rate)
        self.epochs = epochs
        self.TrainDataLoader = train_data_loader
        self.TestDataLoader = test_data_loader

    @staticmethod
    def LossFunction(inputs, targets) -> float:
        loss_function = nn.MSELoss()
        mse_loss = loss_function(inputs, targets)
        return mse_loss

    def Train(self) -> float:
        self.train(mode=True)
        TotalLoss = 0.0

        for batch_index, batch in enumerate(self.TrainDataLoader):
            x_batch, y_batch = batch[0], batch[1]

            output = self.forward(x_batch)
            loss = self.LossFunction(inputs=output[-1], targets=y_batch)
            self.Optimiser.zero_grad()
            loss.backward()
            self.Optimiser.step()
            TotalLoss += loss

        TotalLoss = TotalLoss / len(self.TrainDataLoader)
        return TotalLoss

    def Evaluate(self) -> float:
        self.eval()
        TotalLoss = 0.0

        for batch_index, batch in enumerate(self.TestDataLoader):
            x_batch, y_batch = batch[0], batch[1]

            with torch.no_grad():
                output: torch.Tensor = self.forward(x_batch)
                loss = self.LossFunction(inputs=output[-1], targets=y_batch)
                TotalLoss += loss

        TotalLoss = TotalLoss / len(self.TrainDataLoader)
        return TotalLoss

    def TrainModel(self, early_stopping_iter: int = 10) -> float:
        best_loss = np.inf
        early_stopping_counter: int = 0

        for epoch in range(self.epochs):
            train_loss: float = self.Train()
            valid_loss: float = self.Evaluate()

            print(f'EPOCH: {epoch} | TRAIN LOSS: {train_loss} | VALIDATE LOSS: {valid_loss}')

            if valid_loss < best_loss:
                best_loss = valid_loss
            else:
                early_stopping_counter += 1
            if early_stopping_counter >= early_stopping_iter: break

        return float(best_loss)

    def Predict(self, batch) -> list[float]:
        self.eval()
        output: Tensor = self.forward(batch)
        output: list[float] = list(output[-1][-1].detach().numpy())
        return output
