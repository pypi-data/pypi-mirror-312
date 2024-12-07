from typing import Any
import optuna
from optuna import *
from torch import Tensor

from datafeeder import DataFeederModel
from sideclasses import DataBatch
from DataEngine import DataEngineModel
from LongShortTremMemoryEngine import LongShortTermMemoryEngineModel


class DeepLearningEngineModel:
    def __init__(self, data_engine: DataEngineModel, symbol_name: str, num_trials: int=2) -> None:
        self.DataEngineModel = data_engine
        self.storage = f"sqlite:///:memory:/{symbol_name}.db"
        self.study_name: str = symbol_name
        self.num_trials: int = num_trials
    
    def Objective(self, trial):
        params = {
            "epochs": trial.suggest_int("epochs", 10, 15),
            "hidden_size": trial.suggest_int("hidden_size", 2, 32),
            "num_layers": trial.suggest_int("num_layers", 2, 10),
            "num_linear_connections": trial.suggest_int("num_linear_connections", 128, 256), 
            "dropout": trial.suggest_uniform("dropout", 0.01, 0.1), 
            "learning_rate": trial.suggest_loguniform("learning_rate", 0.00001, 0.001)
        }

        feeder: DataFeederModel = self.DataEngineModel.GetFeeder(symbol=self.study_name)
        train_data_loader, test_data_loader = feeder.DataLoaders()

        long_short_term_memory_engine_model: LongShortTermMemoryEngineModel = LongShortTermMemoryEngineModel(
            epochs=params["epochs"],
            num_classes_output=8, 
            input_size=76,
            hidden_size=params["hidden_size"],
            num_layers=params["num_layers"],
            num_linear_connections=params["num_linear_connections"],
            dropout=params["dropout"],
            learning_rate=params["learning_rate"],
            train_data_loader=train_data_loader,
            test_data_loader=test_data_loader
        )
        return long_short_term_memory_engine_model.TrainModel()

    def OptimizeModel(self):
        study = optuna.create_study(study_name=self.study_name, direction='minimize')
        return study
    
    def Predict(self) -> list[float]:
        study = self.OptimizeModel()
        if self.DataEngineModel.IS_ENGINE_READY(symbol=self.study_name):

            study.optimize(self.Objective, self.num_trials)
            best_params: dict[str, Any] = study.best_params

            feeder: DataFeederModel = self.DataEngineModel.GetFeeder(symbol=self.study_name)
            train_data_loader, test_data_loader = feeder.DataLoaders()

            long_short_term_memory_engine_model: LongShortTermMemoryEngineModel = LongShortTermMemoryEngineModel(
                epochs=best_params["epochs"],
                num_classes_output=8, 
                input_size=76,
                hidden_size=best_params["hidden_size"],
                num_layers=best_params["num_layers"],
                num_linear_connections=best_params["num_linear_connections"],
                dropout=best_params["dropout"],
                learning_rate=best_params["learning_rate"],
                train_data_loader=train_data_loader,
                test_data_loader=test_data_loader
            )
            long_short_term_memory_engine_model.TrainModel()

            last_input_tensor: Tensor = feeder.LAST_INPUT_TENSOR
            return long_short_term_memory_engine_model.Predict(batch=last_input_tensor)
        else: pass

    def Update(self, data_batch: DataBatch): 
        self.DataEngineModel.UpdateDataBase(symbol=self.study_name, data=data_batch)

    @property
    def IS_ENGINE_READY(self):
        is_engine_ready = self.DataEngineModel.IS_ENGINE_READY(symbol=self.study_name)
        if is_engine_ready: return True
        else: return False

