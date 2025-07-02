import pandas as pd
import numpy as np
from pathlib import Path
from src.FaultDetectionTPIM.logger import logging
from src.FaultDetectionTPIM.exception import CustomException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from pathlib import Path
import os

class DataIngestion:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")

        try:
            #reading data
            data=pd.read_csv(Path(os.path.join("notebooks/data", "predictive_maintenance.csv")))
            logging.info("i have read dataset as df")

            #splitting data
            logging.info("Here i have performed train test split")
            train_data,test_data=train_test_split(data, test_size=0.25)
            logging.info("Here train test split completed")

        except Exception as e:    
            pass
     
