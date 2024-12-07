from copy import deepcopy as dc

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pandas import DataFrame
import pandas as pd
import yfinance
import torch


def get_device() -> str:
    """returns the available device"""
    device: str = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    return device


def convert_date_index_to_datetime(dataframe: DataFrame) -> DataFrame:
    """convert the `Date` str index to a datetime obj"""
    copied_dataframe: DataFrame = dc(dataframe)
    copied_dataframe.index = pd.to_datetime(copied_dataframe.index)
    return copied_dataframe


def get_labels_by_targets(dataframe: DataFrame, target: str = 'Close') -> tuple:
    labels, targets = dataframe.drop(columns=[target]), dataframe.Close.values
    return labels, targets


if __name__ == '__main__':
    from scaler import DataFrameStandardisingScaler
    from dataframe_shifter import DataFrameShifter
    from train_test_split import TrainTestSplit

    # get the historical data
    msft_data = yfinance.Ticker("MSFT")
    msft_data_df = msft_data.history(period="max")
    msft_data_df.pop('Dividends')
    msft_data_df.pop('Stock Splits')

    msft_data_df = convert_date_index_to_datetime(dataframe=msft_data_df)
    labels, targets = get_labels_by_targets(dataframe=msft_data_df)
    scaler = DataFrameStandardisingScaler(labels=labels, targets=targets)
    shifter = DataFrameShifter(
        input_sequences=scaler.transformed_labels,
        output_sequence=scaler.transformed_targets,
        num_steps_backwards=64,
        num_steps_forwards=14
    )
    labels_seq, targets_seq = shifter.labels_sequence, shifter.targets_sequence
    spliter = TrainTestSplit(labels=labels_seq, targets=targets_seq)
