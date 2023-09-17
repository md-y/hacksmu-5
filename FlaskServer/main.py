from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import openai
import pandas as pd
import json
from apikey import api_key
import numpy as np
from sklearn.neighbors import NearestNeighbors
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

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

def extract_features_with_id(asset):
    asset_id = int(asset['Asset ID'])
    
    # Extract Operational Time, handle if it's not an integer
    try:
        operational_time = int(asset['Operational Time (hrs)'])
    except ValueError:
        operational_time = 0
    
    # Extract other fields and handle potential missing values
    features = {
        'Asset ID': asset_id,
        'Operational Time (hrs)': operational_time,
        'Criticality Level': asset.get('Criticality Level', 0),
        'Cost': asset.get('Cost', 0),
        'Energy Efficiency': asset.get('Energy Efficiency', 0),
        'Weight': asset.get('Weight', 0),
        'Height From Floor': asset.get('Height From Floor', 0),
        'Number of Service Reports': len(asset.get('Service Reports', [])),
        'Number of Work Orders': len(asset.get('Work Orders', []))
    }
    return features

# Create a matrix of features including Asset ID
feature_matrix_with_id = [extract_features_with_id(asset) for asset in json_data]
df_with_id = pd.DataFrame(feature_matrix_with_id)
df_with_id.set_index("Asset ID", inplace=True)

# Using NearestNeighbors on the dataframe
k = 5
nn = NearestNeighbors(n_neighbors=k + 1)
nn.fit(df_with_id)
distances, indices = nn.kneighbors(df_with_id)
anomaly_scores = distances[:, -1]
sorted_scores_idx = np.argsort(-anomaly_scores)

# Considering top 5% as anomalies
num_anomalies = int(0.05 * len(df_with_id))
anomaly_indices = sorted_scores_idx[:num_anomalies]

# Store anomalies in a set for quick look-up
anomaly_asset_ids = set(df_with_id.iloc[anomaly_indices].index)

def is_anomaly(asset_id):
    return asset_id in anomaly_asset_ids

def average_service_interval(service_dates):
    if len(service_dates) < 2:
        return None
    service_dates = [datetime.strptime(date['Date Serviced'], '%m/%d/%Y') for date in service_dates]
    service_dates.sort()
    intervals = [(service_dates[i+1] - service_dates[i]).days for i in range(len(service_dates)-1)]
    return sum(intervals) / len(intervals)

def extract_features(asset):
    features = {
        'Operational Time (hrs)': int(asset['Operational Time (hrs)']),
        'Criticality Level': int(asset['Criticality Level']),
        'Cost': int(asset['Cost']),
        'Energy Efficiency': int(asset['Energy Efficiency']),
        'Weight': int(asset['Weight']),
        'Height From Floor': int(asset['Height From Floor']),
        'Average Time Between Services': average_service_interval(asset.get('Service Reports', [])),
        'Number of Service Reports': len(asset.get('Service Reports', [])),
        'Number of Work Orders': len(asset.get('Work Orders', []))
    }
    return features

def extract_target(asset):
    if 'Service Reports' in asset and asset['Service Reports']:
        last_service_date = datetime.strptime(asset['Service Reports'][-1]['Date Serviced'], '%m/%d/%Y')
        average_interval = average_service_interval(asset['Service Reports'])
        if average_interval:
            predicted_next_service_date = last_service_date + timedelta(days=average_interval)
            days_until_next_service = (predicted_next_service_date - last_service_date).days
            return days_until_next_service
    return None

def train_service_regressor(data):
    features_list = [extract_features(asset) for asset in data]
    target_list = [extract_target(asset) for asset in data]
    valid_indices = [i for i, target in enumerate(target_list) if target is not None]
    df_features = pd.DataFrame([features_list[i] for i in valid_indices])
    df_target = pd.Series([target_list[i] for i in valid_indices])

    for column in df_features.columns:
        if df_features[column].isnull().sum() > 0:
            mean_value = df_features[column].mean()
            df_features[column].fillna(mean_value, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_service_date(asset_id, model, data):
    asset = next((item for item in data if int(item['Asset ID']) == int(asset_id)), None)
    if asset is None:
        return f"No asset found with Asset ID: {asset_id}"
    
    features = extract_features(asset)
    features_df = pd.DataFrame([features])
    
    days_until_next_service = model.predict(features_df)[0]
    last_service_date = datetime.strptime(asset['Service Reports'][-1]['Date Serviced'], '%m/%d/%Y')
    predicted_date = last_service_date + timedelta(days=int(days_until_next_service))
    return predicted_date.strftime('%m/%d/%Y')

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

model = train_service_regressor(json_data)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/next_asset', methods=['GET'])
@cross_origin()
def next_asset():
    doc_count = collection.count_documents({})
    result = {"response": doc_count}
    return result

@app.route('/asset', methods=['GET'])
@cross_origin()
def search_asset():
    args = request.args
    id = args.get("id")
    
    result = collection.find_one(filter={"Asset ID": int(id)})
    result['_id'] = str(result['_id'])  # Convert ObjectId to string
    return jsonify(result)

@app.route('/post_asset', methods=['POST'])
@cross_origin()
def post_asset():
    data = json.loads(str(request.data)[2:-1])
    collection.replace_one({"Asset ID": int(data["Asset ID"])}, data, True)
    return {"status": "success"}

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

@app.route('/anomaly', methods=['GET'])
@cross_origin()
def check_anomaly():
    asset_id = request.args.get("id")
    result = {"response": is_anomaly(asset_id)}
    return jsonify(result)

@app.route('/serviceRegression', methods=['GET'])
@cross_origin()
def service_regression():
    asset_id = request.args.get("id")    
    predicted_date = predict_service_date(asset_id, model, json_data)
    result = {"response": predicted_date}
    return jsonify(result)

if __name__ == "__main__":
    app.run()
