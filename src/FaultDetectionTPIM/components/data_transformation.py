import sys
import os
import pandas as pd
import numpy as np
from src.FaultDetectionTPIM.logger import logging
from src.FaultDetectionTPIM.exception import CustomException
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from src.FaultDetectionTPIM.utils import save_object
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, RobustScaler
import pandas as pd
from utils.utils import get_logger

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation.config=DataTransformationConfig()

        

    def get_data_transformation(self):
        try:
            logging.info("Data_transformation initiated")
            #defining which column should be ordinal-encoded and which should be scaled
            categorical_cols=[] #fill list
            numerical_cols=[]    #fill list

            # define custum rankings for each ordinal variable
            categories1=[]
            #categories2=[]
            #categories3=[]

            logging.info("pipeline initiated")

            #numerical pipeline
            num_pipeline=Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            #categorical pipeline
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder',OrdinalEncoder(categories=[])), #fill list
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols),
            ])

            return preprocessor
        except Exception as e:
            logging.info("Exception occured in the get_data_transformation")

            raise CustomException(e,sys)
        
       

    def clean_and_encode(df):
        logger = get_logger('DataTransformation')
        try:
            df = df.drop(['UDI', 'Product ID'], axis=1)
            df = df.rename(columns={
                'Air temperature [K]': 'Air temperature',
                'Process temperature [K]': 'Process temperature',
                'Rotational speed [rpm]': 'Rotational speed',
                'Torque [Nm]': 'Torque',
                'Tool wear [min]': 'Tool wear'
            })
            failure_types = df['Failure Type'].unique().tolist()
            ord_enc = OrdinalEncoder(categories=[['L','M','H'], failure_types])
            enc = ord_enc.fit_transform(df[['Type', 'Failure Type']])
            df.drop(['Type', 'Failure Type'], axis=1, inplace=True)
            df[['Type', 'Failure Type']] = enc
            return df
        except Exception as e:
            logger.error(f"Error in clean_and_encode: {e}")
            raise

    def scale_features(df):
        logger = get_logger('DataTransformation')
        try:
            robust_cols = ['Rotational speed', 'Torque']
            scaler_robust = RobustScaler()
            df[robust_cols] = scaler_robust.fit_transform(df[robust_cols])

            minmax_cols = ['Air temperature', 'Process temperature', 'Tool wear']
            scaler_minmax = MinMaxScaler()
            df[minmax_cols] = scaler_minmax.fit_transform(df[minmax_cols])
            return df
        except Exception as e:
            logger.error(f"Error in scale_features: {e}")
            raise


    def initialize_data_transformation(self,train_path, test_path):   
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Reading train and test data completed")
            logging.info(f'Train dataframe head: /n{train_df.head().to_string()}')
            logging.info(f'Test dataframe head: /n{test_df.head().to_string()}')

            preprocessing_obj = self.get_data_transformation()

            target_column_name=['target','failure_type']
            drop_columns=[target_column_name,'id']

            input_feature_train_df= train_df.drop(columns=drop_columns,axis=1)
            input_feature_test_df= test_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]
            target_feature_test_df=test_df[target_column_name]

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            #for validation
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test_df)
            logging.info("Applying preprocessing object on training and test datasets")
            train_arr= np.c_(input_feature_train_arr, np.array( target_feature_train_df))
            test_arr=np.c_(input_feature_test_arr,np.array(target_feature_test_df))
            #saving the preprocessing pickle file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("preprocessor picle file saved")

            return (
                train_arr,
                test_arr
            )
        except Exception as e:
            logging.info("Exception occured in the initiate_data_transformation")
            raise CustomException(e,sys)

