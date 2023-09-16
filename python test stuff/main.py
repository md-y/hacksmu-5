from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6706186085905149183.pem',
                     server_api=ServerApi('1'))

db = client['testDB']
collection = db['testCol']
doc_count = collection.count_documents({})
print(doc_count)
