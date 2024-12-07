from pandas import DataFrame

from .util import convert_date_index_to_datetime, get_labels_by_targets, get_device
from .dataset import LSTMStockMarketTimeSeriesDataSet
from .scaler import DataFrameStandardisingScaler
from .train_test_spliter import TrainTestSpliter
from .dataframe_shifter import DataFrameShifter
from .data_loader import get_data_loader


def prepare_dataframe(dataframe: DataFrame, num_steps_backwards: int, num_steps_forwards: int) -> TrainTestSpliter:
    try:
        dataframe.pop('Dividends')
        dataframe.pop('Stock Splits')

    except:
        print('Something went wrong!')

    converted_dataframe: DataFrame = convert_date_index_to_datetime(dataframe=dataframe)
    labels, targets = get_labels_by_targets(dataframe=converted_dataframe)
    scaler: DataFrameStandardisingScaler = DataFrameStandardisingScaler(labels=labels, targets=targets)
    transformed_labels = scaler.transformed_labels
    transformed_targets = scaler.transformed_targets

    shifter: DataFrameShifter = DataFrameShifter(
        input_sequences=transformed_labels,
        output_sequence=transformed_targets,
        num_steps_backwards=num_steps_backwards,
        num_steps_forwards=num_steps_forwards
    )
    labels_seq, targets_seq = shifter.labels_sequence, shifter.targets_sequence
    spliter: TrainTestSpliter = TrainTestSpliter(labels=labels_seq, targets=targets_seq)
    return spliter
