import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Load the dataset
with open("/Users/jayeshpaluru/Downloads/HackSMU/hacksmu-5/Dataset Creation/dataset.json", "r") as file:
    data = json.load(file)

# Extract numerical features and Asset ID to represent each asset
def extract_features_with_id(asset):
    asset_id = str(asset['Asset ID'])
    
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
feature_matrix_with_id = [extract_features_with_id(asset) for asset in data]
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

# Ask the user for an Asset ID and inform them if it's an anomaly
user_input = input("Please enter an Asset ID: ")

if user_input in anomaly_asset_ids:
    print(f"The Asset ID {user_input} is an anomaly.")
else:
    print(f"The Asset ID {user_input} is not an anomaly.")
