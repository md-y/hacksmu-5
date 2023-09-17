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
    features = {
        'Operational Time (hrs)': asset['Operational Time (hrs)']['$numberInt'],
        'Criticality Level': asset['Criticality Level']['$numberInt'],
        'Cost': asset['Cost']['$numberInt'],
        'Energy Efficiency': asset['Energy Efficiency']['$numberInt'],
        'Weight': asset['Weight']['$numberInt'],
        'Height From Floor': float(asset['Height From Floor']['$numberDouble']) if '$numberDouble' in asset['Height From Floor'] else asset['Height From Floor']['$numberInt'],
        'Average Time Between Services': average_service_interval(asset['Service Reports']),
        'Number of Service Reports': len(asset['Service Reports']),
        'Number of Work Orders': len(asset['Work Orders'])
    }
    return features

# Extract target variable: number of days until the next service
def extract_target(asset):
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

# Predicting the number of days until the next service for all assets
days_until_next_service_predictions = model.predict(df_features)

# Adding the predicted number of days to the last service date to get the predicted next service date
predicted_next_service_dates = {}
for idx, asset in enumerate(data):
    last_service_date = datetime.strptime(asset['Service Reports'][-1]['Date Serviced'], '%m/%d/%Y')
    predicted_date = last_service_date + timedelta(days=int(days_until_next_service_predictions[idx]))
    asset_id = asset['Asset ID']['$numberInt']
    predicted_next_service_dates[asset_id] = predicted_date.strftime('%m/%d/%Y')

# Print the dictionary with Asset ID and their predicted next service dates
for asset_id, date in predicted_next_service_dates.items():
    print(f"Asset ID: {asset_id}, Predicted Next Service Date: {date}")