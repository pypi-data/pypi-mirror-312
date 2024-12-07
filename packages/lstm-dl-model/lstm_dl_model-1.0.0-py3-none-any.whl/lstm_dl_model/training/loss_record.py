
class LossRecord:
    def __init__(self) -> None:
        self._losses: list[float] = list()

    def append_loss(self, loss: float) -> None:
        self._losses.append(loss)

    @property
    def average_loss(self) -> float:
        avg_loss: float = sum(self._losses) / len(self._losses)
        return avg_loss

    @property
    def highest_loss(self) -> float:
        return max(self._losses)

    @property
    def lowest_loss(self) -> float:
        return min(self._losses)


class LossRecordGather:
    def __init__(self) -> None:
        self._loss_records: list[LossRecord] = list()

    def append_loss_record(self, loss_record: LossRecord) -> None:
        self._loss_records.append(loss_record)

    @property
    def average_loss(self) -> float:
        _avg_losses: list[float] = [record.average_loss for record in self._loss_records]
        avg_loss: float = sum(_avg_losses) / len(_avg_losses)
        return avg_loss

    @property
    def best_loss(self) -> float:
        _avg_losses: list[float] = [record.average_loss for record in self._loss_records]
        best_loss: float = min(_avg_losses)
        return
