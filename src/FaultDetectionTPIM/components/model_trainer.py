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


from models.balanced_rf_model import train_balanced_rf
from models.balanced_bagging_model import train_balanced_bagging
from models.balanced_bagging_tomek_model import train_balanced_bagging_tomek
from utils.metrics import evaluate_model
from sklearn.model_selection import train_test_split
import yaml

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

THRESHOLD = config['threshold']

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
