import pandas as pd
import numpy as np
from pathlib import Path
from src.FaultDetectionTPIM.logger import logging
from src.FaultDetectionTPIM.exception import CustomException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from pathlib import Path
import sys
import os

class DataIngestionConfig:
    raw_data_path:str= os.path.join("artifacts","raw.csv")
    train_data_path:str= os.path.join("artifacts","train.csv")
    test_data_path:str= os.path.join("artifacts","test.csv")
class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")

        try:
            #reading data
            data=pd.read_csv(Path(os.path.join("notebooks/data", "predictive_maintenance.csv")))
            logging.info("i have read dataset as df")
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)), exist_ok=True)#only providing artifacts folder
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("i have saved dataset as raw_data in artifacts folder")

            #splitting data
            logging.info("Here i have performed train test split")
            train_data,test_data=train_test_split(data, test_size=0.25)
            logging.info("Here train test split completed")

            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Here train and test data saved in artifacts folder, data ingestion part completed")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:    
            logging.info("exception occured during data ingestion ")
            raise CustomException(e,sys)
     
