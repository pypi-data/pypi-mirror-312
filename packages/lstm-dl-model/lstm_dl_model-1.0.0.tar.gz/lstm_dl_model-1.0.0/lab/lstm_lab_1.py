from copy import deepcopy as dc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print(device)


# get the historical data
msft_data = yfinance.Ticker("MSFT")
msft_data_df = msft_data.history(period="max")
# adjust the DF to be Date : Close
msft_df = msft_data_df[['Close']]
# print(msft_df.index)


def prepare_df_for_lstm(dataframe: pd.DataFrame, num_steps_backwards: int) -> pd.DataFrame:
    df = dc(dataframe)
    # convert the `Date` str to a datetime obj
    df.index = pd.to_datetime(df.index)
    DATE = df.index
    CLOSE = df['Close']

    for i in range(1, num_steps_backwards+1):
        df[f'Close(t-{i})'] = df['Close'].shift(i)

    df.dropna(inplace=True)
    return df


LOOKBACK = 7
shifted_df = prepare_df_for_lstm(dataframe=msft_df, num_steps_backwards=LOOKBACK)
print(shifted_df)

shifted_df_as_np = shifted_df.to_numpy()
print(shifted_df_as_np)


x_data = shifted_df_as_np[:, 1:]
y_data = shifted_df_as_np[:, 0]
print(x_data.shape, y_data.shape)

x_data = dc(np.flip(x_data, axis=1))
print(x_data)

split_index = int(len(x_data) * 0.9)
print(split_index)

x_data_train = x_data[:split_index]
x_data_test = x_data[split_index:]
y_data_train = y_data[:split_index]
y_data_test = y_data[split_index:]
print(x_data_train.shape, x_data_test.shape, y_data_train.shape, y_data_test.shape)

# reshaping
x_data_train = x_data_train.reshape((-1, LOOKBACK, 1))
x_data_test = x_data_test.reshape((-1, LOOKBACK, 1))
y_data_train = y_data_train.reshape((-1, 1))
y_data_test = y_data_train.reshape((-1, 1))
print(x_data_train.shape, x_data_test.shape, y_data_train.shape, y_data_test.shape)


x_data_train = torch.tensor(x_data_train).float()
x_data_test = torch.tensor(x_data_test).float()
y_data_train = torch.tensor(y_data_train).float()
y_data_test = torch.tensor(y_data_test).float()
print(x_data_train.shape, x_data_test.shape, y_data_train.shape, y_data_test.shape)


class TimeSeriesDataSet(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, item):
        return self.x_data[item], self.y_data[item]


train_dataset: TimeSeriesDataSet = TimeSeriesDataSet(x_data_train, y_data_train)
test_dataset: TimeSeriesDataSet = TimeSeriesDataSet(x_data_test, y_data_test)


BATCH_SIZE = 16

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)


for _, batch in enumerate(train_loader):
    x_batch, y_batch = batch[0].to(device), batch[1].to(device)
    print(x_batch.shape, y_batch.shape)
    break
