from sklearn.preprocessing import StandardScaler, MinMaxScaler


class BaseScaler:
    _standard_scaler = StandardScaler()
    _min_max_scaler = MinMaxScaler()


class DataFrameStandardisingScaler(BaseScaler):
    def __init__(self, labels, targets):
        self._transformed_labels = self._standard_scaler.fit_transform(labels)
        self._transformed_targets = self._min_max_scaler.fit_transform(targets.reshape(-1, 1))

    @property
    def transformed_labels(self):
        return self._transformed_labels

    @property
    def transformed_targets(self):
        return self._transformed_targets
