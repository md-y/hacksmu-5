#Code to connect to data base
import json
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import pandas as pd

uri = "mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6706186085905149183.pem',
                     server_api=ServerApi('1'))

db = client['CBREData']
collection = db['CBREData']

#get data
docs = list(collection.find())
df = pd.DataFrame.from_dict(docs)

#make vizualizations
df

