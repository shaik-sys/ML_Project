from housing.entity.config_entity import DataIngestionConfig
from housing.exception import HousingException
import os, sys
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit




class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
            print(self.data_ingestion_config)
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def download_housing_data(self)->str:
        try:
            #extracting remote url to download dataset
            download_url  =self.data_ingestion_config.dataset_download_url
            print(download_url)

            #getting the folder loaction to download the file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            tgz_download_dir= ''.join(tgz_download_dir)
            print(tgz_download_dir)



            
            

            housing_file_name=os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir,housing_file_name
                                         )        
            os.makedirs(tgz_download_dir,exist_ok=True)
            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")

            urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info(f"file :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path
        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            raw_data_dir = ''.join(raw_data_dir)
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extraction Completed")
        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            raw_data_dir = ''.join(raw_data_dir)
            print(raw_data_dir)
            print(os.listdir(raw_data_dir))
            file_name = os.listdir(raw_data_dir)[0]
            #csv file path
            housing_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file:[{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame["income_category"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                labels=[1,2,3,4,5]
            )
            logging.info(f"Splitting data into train and test")
            strat_train_set =None
            strat_test_set =None

            split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)

            for train_index,test_index in split.split(housing_data_frame,housing_data_frame["income_category"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_category"],axis=1)
                strat_test_set=housing_data_frame.loc[test_index].drop(["income_category"],axis=1)


            x=self.data_ingestion_config.ingested_train_dir
            x1 = ''.join(x)
            y=self.data_ingestion_config.ingested_test_dir
            x2 = ''.join(y)
    
            train_file_path=os.path.join(x1,file_name)
            print(train_file_path)
            test_file_path=os.path.join(x2,file_name)
            print(test_file_path)

            ing_train = self.data_ingestion_config.ingested_train_dir
            ing_train1 = ''.join(ing_train)
            ing_test = self.data_ingestion_config.ingested_test_dir
            ing_test1 = ''.join(ing_test)

            if strat_train_set is not None:
                
                os.makedirs(ing_train1,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(ing_test1,exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv( test_file_path,index=False)

            data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
                                  test_file_path=test_file_path,
                                  is_ingested=True,
                                  message="Data Ingestion Completed successfully"
                                  )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
            




            

        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e
        



    def __del__(self):
            logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
        