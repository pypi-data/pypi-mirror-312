from datafeeder import DataFeederModel
from sideclasses import DataBatch


class DataEngineModel:
    def __init__(self, backward_sequence_len: int, forward_sequence_len: int) -> None:
        self.SecurityByDataFeederDataBase: dict[str, DataFeederModel] = dict()
        self.backward_sequence_len: int = backward_sequence_len
        self.forward_sequence_len: int = forward_sequence_len
    
    def AddFeeder(self, symbol: str) -> None:
        is_feeder_exists = self.SecurityByDataFeederDataBase.get(symbol, None)
        if is_feeder_exists is None:
            self.SecurityByDataFeederDataBase[symbol] = DataFeederModel(
                backward_sequence_len=self.backward_sequence_len,
                forward_sequence_len=self.forward_sequence_len
            )
        else: pass

    def UpdateDataBase(self, symbol: str, data: DataBatch) -> None:
        self.AddFeeder(symbol=symbol)
        feeder: DataFeederModel | None = self.SecurityByDataFeederDataBase.get(symbol, None)
        if feeder is not None:
            feeder.Update(data=data)
        else: pass
    
    def GetFeeder(self, symbol: str) -> (DataFeederModel | None):
        feeder: DataFeederModel | None = self.SecurityByDataFeederDataBase.get(symbol, None)
        if feeder is not None: return feeder
        else: pass
    
    def IS_ENGINE_READY(self, symbol: str) -> bool:
        feeder = self.GetFeeder(symbol=symbol)
        if feeder is not None: 
            if feeder.IS_ENGINE_READY: return True
            else: return False
        else: return False

