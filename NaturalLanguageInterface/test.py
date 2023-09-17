import openai
import pandas as pd
from datetime import datetime

# Load the dataset from the JSON file
with open("/Users/jayeshpaluru/Downloads/HackSMU/NaturalLanguageInterface/dataset.json", "r") as file:
    import json
    with open("/Users/jayeshpaluru/Downloads/HackSMU/NaturalLanguageInterface/dataset.json", "r") as file:
        json_data = json.load(file)
data_json = pd.DataFrame(json_data)

# Convert specific nested dictionary fields to their integer or float counterparts
for column in ['Asset ID', 'Floor', 'Room', 'Operational Time (hrs)', 'Criticality Level', 'Time Between Services', 'Cost', 'Energy Efficiency', 'Weight']:
    data_json[column] = data_json[column].apply(lambda x: int(x['$numberInt']) if isinstance(x, dict) and '$numberInt' in x else x)
for column in ['Height From Floor']:
    data_json[column] = data_json[column].apply(lambda x: float(x['$numberDouble']) if isinstance(x, dict) and '$numberDouble' in x else x)

# Set up OpenAI API key
openai.api_key = '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'

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

def chat_with_gpt3_and_dataset_json(user_query):
    context = detailed_summarize_dataset_json()
    combined_input = context + "\n\nUser: " + user_query + "\nAssistant:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a natural language interface for a dataset meant to answer the user's questions with data from the dataset, and make predictions from the data when asked."},
            {"role": "user", "content": combined_input}
        ]
    )
    return response.choices[0].message['content'].strip()

def main_json():
    print("GPT-3.5-Turbo Chatbot with CBRE Dataset Integration (JSON version)\n")
    print("Type 'exit' to end the chat.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            response = chat_with_gpt3_and_dataset_json(user_input)
            print("Chatbot: ", response)

if __name__ == "__main__":
    main_json()
