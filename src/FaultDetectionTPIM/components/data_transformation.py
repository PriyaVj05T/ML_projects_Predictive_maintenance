import sys
import os
import pandas as pd
import numpy
from src.FaultDetectionTPIM.logger import logging
from src.FaultDetectionTPIM.exception import CustomException
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from src.FaultDetectionTPIM.utils import save_object

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

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            #for validation
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test_df)
            logging.info("Applying preprocessing object on training and test datasets")

            #saving the preprocessing pickle file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

        except Exception as e:
            logging.info("Exception occured in the initiate_data_transformation")
            raise CustomException(e,sys)

