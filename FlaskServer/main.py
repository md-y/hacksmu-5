from flask import Flask, request
from flask import jsonify
from flask_cors import CORS, cross_origin
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to MongoDB
uri = "mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6706186085905149183.pem',
                     server_api=ServerApi('1'))

db = client['CBREData']
collection = db['CBREData']

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# ...
@app.route('/asset', methods=['GET'])
@cross_origin()
def search():
    args = request.args
    id = args.get("id")

    result = collection.find_one(filter={"Asset ID": int(id)})
    result['_id'] = ""
    return result