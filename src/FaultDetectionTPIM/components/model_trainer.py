import numpy as np
import pandas as pd
import os
import sys
from dataclasses import dataclass
from src.FaultDetectionTPIM.logger import logging
from src.FaultDetectionTPIM.exception import CustomException
from src.FaultDetectionTPIM.utils import save_object
from src.FaultDetectionTPIM.utils import evaluate_model

from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, RobustScaler
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score, cross_val_predict, StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from imblearn.ensemble import BalancedRandomForestClassifier, BalancedBaggingClassifier
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks


@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self):
        try:
            pass

        except Exception as e:
            logging.info("Exception occur during initiating model training")
            raise CustomException(e,sys)
