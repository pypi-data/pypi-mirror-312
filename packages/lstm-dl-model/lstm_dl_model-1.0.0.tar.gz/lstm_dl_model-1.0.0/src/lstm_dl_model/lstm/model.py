from torch import Tensor
import torch.nn as nn
import torch

from src.lstm_dl_model.data import get_device


class LstmModel(nn.Module):
    def __init__(self, num_classes_output: int, input_size: int, hidden_size: int, num_layers: int, num_linear_connections: int, dropout: float = 0.1) -> None:
        super().__init__()
        self.num_classes: int = num_classes_output  # output size
        self.num_layers: int = num_layers  # number of recurrent layers in the lstm
        self.input_size: int = input_size  # input size
        self.hidden_size: int = hidden_size  # neurons in each lstm layer

        # LSTM model
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)  # lstm
        self.linear_func_1 = nn.Linear(hidden_size, num_linear_connections)  # fully connected
        self.linear_func_2 = nn.Linear(num_linear_connections, num_classes_output)  # fully connected last layer
        self.relu = nn.ReLU()

    def forward(self, x):
        # hidden state
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(get_device())
        # cell state
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(get_device())

        # propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0))  # (input, hidden, and internal state)
        out = self.relu(hn)
        out = self.linear_func_1(out)  # first dense
        out = self.relu(out)  # relu
        out = self.linear_func_2(out)  # final output
        return out

    def predict(self, batch) -> list[float]:
        self.eval()
        output: Tensor = self.forward(batch)
        output: list[float] = list(output[-1][-1].detach().numpy())
        return output

    @staticmethod
    def put_on_device(model: nn.Module):
        # put on available device
        model.to(get_device())


if __name__ == '__main__':
    model = LstmModel(1, 4, 1, 1, 1)
    model.put_on_device(model)
