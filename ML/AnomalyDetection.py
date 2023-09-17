import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Load the dataset
with open("/Users/jayeshpaluru/Downloads/HackSMU/hacksmu-5/Dataset Creation/dataset.json", "r") as file:
    data = json.load(file)

# Extract numerical features and Asset ID to represent each asset
def extract_features_with_id(asset):
    features = {
        'Asset ID': asset['Asset ID']['$numberInt'],
        'Operational Time (hrs)': asset['Operational Time (hrs)']['$numberInt'],
        'Criticality Level': asset['Criticality Level']['$numberInt'],
        'Cost': asset['Cost']['$numberInt'],
        'Energy Efficiency': asset['Energy Efficiency']['$numberInt'],
        'Weight': asset['Weight']['$numberInt'],
        'Height From Floor': float(asset['Height From Floor']['$numberDouble']) if '$numberDouble' in asset['Height From Floor'] else asset['Height From Floor']['$numberInt'],
        'Number of Service Reports': len(asset['Service Reports']),
        'Number of Work Orders': len(asset['Work Orders'])
    }
    return features

# Create a matrix of features including Asset ID
feature_matrix_with_id = [extract_features_with_id(asset) for asset in data]
df_with_id = pd.DataFrame(feature_matrix_with_id)

# Setting "Asset ID" as the index for the dataframe
df_with_id.set_index("Asset ID", inplace=True)

# Using NearestNeighbors on the dataframe
k = 5
nn = NearestNeighbors(n_neighbors=k + 1)
nn.fit(df_with_id)
distances, indices = nn.kneighbors(df_with_id)
anomaly_scores = distances[:, -1]
sorted_scores_idx = np.argsort(-anomaly_scores)
num_anomalies = int(0.05 * len(df_with_id))
anomaly_indices = sorted_scores_idx[:num_anomalies]

# Displaying the anomalies sorted by Asset ID
anomalies_sorted_by_id = df_with_id.iloc[anomaly_indices].sort_index()
print(anomalies_sorted_by_id)
