import json
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import seaborn as sns

# Connect to MongoDB
uri = "mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-6706186085905149183.pem',
                     server_api=ServerApi('1'))

db = client['CBREData']
collection = db['CBREData']

# Get data
docs = list(collection.find())
df = pd.DataFrame.from_dict(docs)
df_operational_logs = pd.json_normalize(docs, record_path='Operational Logs')

# Display dataframe
df
# App title
st.title('MongoDB Data Visualization')

# 4. Metrics Overview
if st.checkbox('Show Distribution of Cost'):
    fig4 = px.box(df, x='Cost', title="Distribution of Cost")
    st.plotly_chart(fig4)


# Create 3D Scatter Plot
if st.checkbox('Show 3D Scatter Plot'):
    fig_3d_scatter = px.scatter_3d(df, 
                               x='Operational Time (hrs)', 
                               y='Cost', 
                               z='Energy Efficiency',
                               color='Asset Type',
                               size='Criticality Level',
                               hover_data=['Manufacturer'],
                               opacity=0.7,
                               title="3D Scatter Plot of Assets based on Operational Time, Cost, and Energy Efficiency")
    # Display the visualization in Streamlit
    st.plotly_chart(fig_3d_scatter)



if st.checkbox('Show Scatter Plot of Cost vs Energy Efficiency'):
    fig_scatter = px.scatter(df, 
                         x='Cost', 
                         y='Energy Efficiency', 
                         color='Asset Type',
                         title="Scatter Plot of Cost vs Energy Efficiency")
    st.plotly_chart(fig_scatter)

if st.checkbox('Show parallel coordinates plot of Operational Time, Cost, and Energy Efficiency'):
    fig_parallel_coordinates = px.parallel_coordinates(df, 
                                                   dimensions=['Operational Time (hrs)', 'Cost', 'Energy Efficiency'],
                                                   title="Parallel Coordinates Plot of Operational Time, Cost, and Energy Efficiency")
    st.plotly_chart(fig_parallel_coordinates)

if st.checkbox('Show violin plot'):
    fig_violin = px.violin(df, 
                       y='Cost', 
                       x='Asset Type', 
                       color='Asset Type',
                       title="Violin Plot of Cost by Asset Type")
    st.plotly_chart(fig_violin)

if st.checkbox('Show bubble chart'):
    fig_bubble = px.scatter(df, x='Operational Time (hrs)', y='Energy Efficiency', size='Cost', color='Asset Type')
    st.plotly_chart(fig_bubble)

if st.checkbox('Show donut chart'):
    fig_donut = px.pie(df, values='Cost', names='Asset Type', hole=.5, title='Donut Chart of Cost by Asset Type')
    st.plotly_chart(fig_donut)

if st.checkbox('Show line chart'):
    fig_line = px.line(df, x='Installation Date', y='Operational Time (hrs)', color='Asset Type')
    st.plotly_chart(fig_line)

if st.checkbox('Show area chart'):
    fig_area = px.area(df, x='Installation Date', y='Operational Time (hrs)', color='Asset Type')
    st.plotly_chart(fig_area)
