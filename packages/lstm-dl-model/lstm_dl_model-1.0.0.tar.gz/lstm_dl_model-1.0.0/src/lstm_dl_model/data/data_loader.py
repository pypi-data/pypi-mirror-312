from torch.utils.data import DataLoader, Dataset


def get_data_loader(dataset: Dataset, batch_size: int, on_train=False) -> DataLoader:
    """
    on_train: wraps to `shuffle` argument in DataLoader

    return: DataLoader
    """
    data_loader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=on_train
    )
    return data_loader
