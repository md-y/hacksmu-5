import json
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the JSON dataset
with open("/Users/jayeshpaluru/Downloads/HackSMU/hacksmu-5/Dataset Creation/dataset.json", "r") as file:
    data = json.load(file)

# Function to calculate the average time between service dates
def average_service_interval(service_dates):
    if len(service_dates) < 2:
        return None
    service_dates = [datetime.strptime(date['Date Serviced'], '%m/%d/%Y') for date in service_dates]
    service_dates.sort()
    intervals = [(service_dates[i+1] - service_dates[i]).days for i in range(len(service_dates)-1)]
    return sum(intervals) / len(intervals)

# Extracting relevant features from the data
def extract_features(asset):
    # Handle cases where the values might be stored as strings by converting them to appropriate data types
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

# Extract target variable: number of days until the next service
def extract_target(asset):
    if 'Service Reports' in asset and asset['Service Reports']:
        last_service_date = datetime.strptime(asset['Service Reports'][-1]['Date Serviced'], '%m/%d/%Y')
        average_interval = average_service_interval(asset['Service Reports'])
        if average_interval:
            predicted_next_service_date = last_service_date + timedelta(days=average_interval)
            days_until_next_service = (predicted_next_service_date - last_service_date).days
            return days_until_next_service
    return None

# Create a dataframe with features and target
df_features = pd.DataFrame([extract_features(asset) for asset in data])
df_target = pd.Series([extract_target(asset) for asset in data if extract_target(asset) is not None])

# Check for missing values in the dataframe and replace them with the mean value of the corresponding feature
for column in df_features.columns:
    if df_features[column].isnull().sum() > 0:
        mean_value = df_features[column].mean()
        df_features[column].fillna(mean_value, inplace=True)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.2, random_state=42)

# Initializing and training the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def predict_service_date(asset_id):
    asset = next((item for item in data if item['Asset ID'] == asset_id), None)
    if asset is None:
        return f"No asset found with Asset ID: {asset_id}"
    
    features = extract_features(asset)
    # Ensure the features are in the same order as during training
    features_df = pd.DataFrame([features])
    features_df = features_df[X_train.columns]
    
    days_until_next_service = model.predict(features_df)[0]
    last_service_date = datetime.strptime(asset['Service Reports'][-1]['Date Serviced'], '%m/%d/%Y')
    predicted_date = last_service_date + timedelta(days=int(days_until_next_service))
    return predicted_date.strftime('%m/%d/%Y')

# Get asset ID from the user
asset_id = int(input("Please enter the Asset ID: "))  # Convert input to integer
predicted_date = predict_service_date(asset_id)
print(f"Predicted Next Service Date for Asset ID {asset_id}: {predicted_date}")
