from torch.nn import MSELoss
from torch.optim import SGD
import yfinance

from training import LstmModelTrainer, get_loss_function, get_optimizer
from data import LSTMStockMarketTimeSeriesDataSet, get_data_loader
from data import prepare_dataframe, TrainTestSpliter
from lstm.model import LstmModel


EPOCHS = 100
LEARNING_RATE = 0.01
INPUT_SIZE = 4
HIDDEN_SIZE = 4
NUM_LAYERS = 2
NUM_CLASSES_OUTPUT = 14
NUM_LINEAR_CONNECTIONS = 2
DROPOUT = 0.1
BATCH_SIZE = 16


def main() -> None:
    # get the historical data
    msft_data = yfinance.Ticker("MSFT")
    msft_data_df = msft_data.history(period="max")
    spliter: TrainTestSpliter = prepare_dataframe(
        dataframe=msft_data_df,
        num_steps_backwards=32,
        num_steps_forwards=14
    )

    train_dataset: LSTMStockMarketTimeSeriesDataSet = LSTMStockMarketTimeSeriesDataSet(
        spliter.train_labels, spliter.train_targets
    )
    test_dataset: LSTMStockMarketTimeSeriesDataSet = LSTMStockMarketTimeSeriesDataSet(
        spliter.test_labels, spliter.test_targets
    )

    train_data_loader: DataLoader = get_data_loader(
        dataset=train_dataset,
        batch_size=BATCH_SIZE,
        on_train=True
    )
    test_data_loader: DataLoader = get_data_loader(
        dataset=test_dataset,
        batch_size=BATCH_SIZE,
        on_train=False
    )

    lstm: LstmModel = LstmModel(
        num_classes_output=NUM_CLASSES_OUTPUT,
        input_size=INPUT_SIZE,
        hidden_size=HIDDEN_SIZE,
        num_layers=NUM_LAYERS,
        num_linear_connections=NUM_LINEAR_CONNECTIONS,
        dropout=DROPOUT
    )
    loss_func = get_loss_function(loss_func=MSELoss)
    optimizer = get_optimizer(
        optim=SGD,
        model_parameters=lstm.parameters(),
        learning_rate=LEARNING_RATE
    )
    trainer = LstmModelTrainer(
        model=lstm,
        epochs=EPOCHS,
        loss_func=loss_func,
        optimizer=optimizer,
        train_data_loader=train_data_loader,
        test_data_loader=test_data_loader
    )
    trainer.train()


if __name__ == '__main__':
    main()
