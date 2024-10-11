import pandas as pd
from database_connect import mongo_operation as mongo 
import os, sys
from src.constants import *
from src.exception import CustomException



class MongoIO:      #this class is used to interact with mongodb database for storing and retereiving product reviews
    mongo_ins = None    #class level variable -> to establish only once during the lifetime of the applications

    def __init__(self):
        if MongoIO.mongo_ins is None:
            mongo_db_url = "mongodb+srv://dpkkr:admin_dpk@cluster0.fv0lm61.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
            MongoIO.mongo_ins = mongo(client_url=mongo_db_url,
                                      database_name=MONGO_DATABASE_NAME)
        self.mongo_ins = MongoIO.mongo_ins

    def store_reviews(self,
                      product_name: str, reviews: pd.DataFrame):   #function to store the reviews scrapped from website
        try:
            collection_name = product_name.replace(" ", "_")
            self.mongo_ins.bulk_insert(reviews,
                                       collection_name)

        except Exception as e:
            raise CustomException(e, sys)

    def get_reviews(self,
                    product_name: str):  #fn used to fetch and generate analysis from the reviews
        try:
            data = self.mongo_ins.find(
                collection_name=product_name.replace(" ", "_")
            )

            return data

        except Exception as e:
            raise CustomException(e, sys)


