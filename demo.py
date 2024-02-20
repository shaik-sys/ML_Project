
from housing.exception import HousingException
from housing.logger import logging


from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation

import os,sys
from housing.pipeline.pipeline import Pipeline





def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        #pipeline.run_pipeline()
        pipeline.start()
        

        logging.info("main function execution completed.")
        # data_validation_config = Configuration().get_data_transformation_config()
        # print(data_validation_config)
        # schema_file_path = r"D:\projects\ML_Project\config\schema.yaml"
        # file_path =r"D:\projects\ML_Project\housing\artifact\data_ingestion\2024-01-09_08-17-23\ingested_data\train\housing.csv"
        # df =DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)



    except Exception as e:
        logging.info(f"{e}")
        print(e)



if __name__ =="__main__":
    main()