import streamlit as st
import pandas as pd
import numpy as np
import json

# Load data
@st.cache
def load_data():
    with open("/Users/jayeshpaluru/Downloads/HackSMU/hacksmu-5/Dataset Creation/dataset.json", "r") as file:
        data = json.load(file)
    return data

def get_asset_by_id(asset_id, data):
    """Retrieve asset details by ID."""
    for asset in data:
        if asset["Asset ID"] == asset_id:
            return asset
    return None

def logs_over_time(asset):
    """Get counts of error and operational logs over time."""
    error_logs = pd.DataFrame(asset['Error Logs'])
    operational_logs = pd.DataFrame(asset['Operational Logs'])
    
    if 'Log Date' in error_logs.columns:
        error_logs['Log Date'] = pd.to_datetime(error_logs['Log Date'])
        error_counts = error_logs.groupby('Log Date').size().resample('M').sum()
    else:
        error_counts = pd.Series(dtype=int)
    
    if 'Log Date' in operational_logs.columns:
        operational_logs['Log Date'] = pd.to_datetime(operational_logs['Log Date'])
        operational_counts = operational_logs.groupby('Log Date').size().resample('M').sum()
    else:
        operational_counts = pd.Series(dtype=int)
        
    return error_counts, operational_counts

def asset_characteristics(asset):
    """Get asset characteristics for visualization."""
    characteristics = {
        'Energy Efficiency': asset['Energy Efficiency'],
        'Weight': asset['Weight'],
        'Height From Floor': asset['Height From Floor']
    }
    return characteristics

data = load_data()

# Select Asset ID
asset_ids = [asset["Asset ID"] for asset in data]
selected_id = st.selectbox('Select Asset ID', asset_ids)

# Retrieve asset details
asset = get_asset_by_id(selected_id, data)



# Logs Over Time
error_counts, operational_counts = logs_over_time(asset)
st.write("### Logs Over Time")
st.line_chart(pd.DataFrame({
    'Error Logs': error_counts,
    'Operational Logs': operational_counts
}))

# Asset Characteristics
characteristics = asset_characteristics(asset)
st.write("### Asset Characteristics")
st.bar_chart(pd.DataFrame({
    'Characteristic': list(characteristics.keys()),
    'Value': list(characteristics.values())
}).set_index('Characteristic'))
