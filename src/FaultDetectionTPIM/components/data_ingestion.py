import pandas as pd
import numpy as np
from pathlib import Path
from src.FaultDetectionTPIM.logger import logging
import os

class DataIngestion:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")

        try:
            #reading data
            pd.read_csv(Path(os.path.join("notebooks\data\predictive_maintenance.csv")))
            logging.info("i have read dataset as df")

            #splitting data

            logging.info("Here i have performed train test split")

        except Exception as e:    
            pass
     
