from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import openai
import pandas as pd
import json
from apikey import api_key

# Load the dataset from the JSON file for chatbot
with open("../Dataset Creation/dataset.json", "r") as file:
    json_data = json.load(file)
data_json = pd.DataFrame(json_data)

# Convert specific nested dictionary fields to their integer or float counterparts
for column in ['Asset ID', 'Floor', 'Room', 'Operational Time (hrs)', 'Criticality Level', 'Time Between Services', 'Cost', 'Energy Efficiency', 'Weight']:
    data_json[column] = data_json[column].apply(lambda x: int(x['$numberInt']) if isinstance(x, dict) and '$numberInt' in x else x)
for column in ['Height From Floor']:
    data_json[column] = data_json[column].apply(lambda x: float(x['$numberDouble']) if isinstance(x, dict) and '$numberDouble' in x else x)

# Connect to MongoDB for assets
uri = "mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6706186085905149183.pem',
                     server_api=ServerApi('1'))
db = client['CBREData']
collection = db['CBREData']

# Set up OpenAI API key
openai.api_key = api_key

def detailed_summarize_dataset_json():
    """Generate a comprehensive summary of the dataset for the chatbot's context."""
    total_assets = len(data_json)
    asset_type_counts = data_json['Asset Type'].value_counts().to_dict()
    asset_type_summary = ', '.join([f"{k} ({v})" for k, v in asset_type_counts.items()])
    manufacturer_counts = data_json['Manufacturer'].value_counts().to_dict()
    manufacturer_summary = ', '.join([f"{k} ({v})" for k, v in manufacturer_counts.items()])
    unique_floors = data_json['Floor'].nunique()
    unique_rooms = data_json['Room'].nunique()
    total_work_orders = data_json['Work Orders'].apply(len).sum()
    total_repairs = data_json['Service Reports'].apply(len).sum()
    avg_operational_time = data_json['Operational Time (hrs)'].mean() / 24  # Convert hours to days
    summary = f"""
    The building contains a total of {total_assets} assets. 
    The assets are distributed among types as: {asset_type_summary}.
    They are manufactured by: {manufacturer_summary}.
    These assets are spread across {unique_floors} unique floors and {unique_rooms} unique rooms.
    The total work orders and repairs for these assets amount to {total_work_orders} and {total_repairs} respectively.
    The average operational time of the assets is approximately {avg_operational_time:.2f} days.
    """
    return summary

def chat_with_gpt3_retaining_knowledge_and_history(user_query, conversation_history):
    """
    Chat with the GPT-3 model, maintaining a history of the conversation and retaining knowledge of the dataset.
    """
    conversation_history.append({"role": "user", "content": user_query})
    
    if len(conversation_history) == 1:
        conversation_history.insert(0, {"role": "system", "content": "You are a natural language interface for a dataset meant to answer the user's questions with data from the dataset, and make predictions from the data when asked. " + detailed_summarize_dataset_json()})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    
    response_text = response.choices[0].message['content'].strip()
    conversation_history.append({"role": "assistant", "content": response_text})
    
    return response_text, conversation_history

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/asset', methods=['GET'])
@cross_origin()
def search_asset():
    args = request.args
    id = args.get("id")
    
    result = collection.find_one(filter={"Asset ID": int(id)})
    result['_id'] = str(result['_id'])  # Convert ObjectId to string
    return jsonify(result)

@app.route('/gpt', methods=['GET'])
@cross_origin()
def search_gpt():
    args = request.args
    prompt = args.get("prompt")
    
    # Get the response from GPT-3 based on the prompt
    conversation_history = []
    response, _ = chat_with_gpt3_retaining_knowledge_and_history(prompt, conversation_history)
    result = {"response": response}
    return jsonify(result)

@app.route('/anamoly', methods=['GET'])
@cross_origin()
def search_gpt():
    args = request.args
    id = args.get("id")
    
    #get result
    result = {"response": False}
    return jsonify(result)

@app.route('/serviceRegression', methods=['GET'])
@cross_origin()
def search_gpt():
    args = request.args
    id = args.get("id")
    
    #get result
    result = {"response": False}
    return jsonify(result)

if __name__ == "__main__":
    app.run()
