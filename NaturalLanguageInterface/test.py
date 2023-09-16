import openai
import pandas as pd
from datetime import datetime

# Load the dataset
data = pd.read_csv('/Users/jayeshpaluru/Downloads/HackSMU/Dataset_-_CBRE_Challenge_-_HackSMU_2023 (1).csv')

# Set up OpenAI API key
openai.api_key = 'OPENAI_API_KEY_HERE'

def detailed_summarize_dataset():
    """Generate a comprehensive summary of the dataset for the chatbot's context."""
    
    # General attributes and specific counts
    total_assets = len(data)
    asset_type_counts = data['Asset Type'].value_counts().to_dict()
    asset_type_summary = ', '.join([f"{k} ({v})" for k, v in asset_type_counts.items()])
    manufacturer_counts = data['Manufacturer'].value_counts().to_dict()
    manufacturer_summary = ', '.join([f"{k} ({v})" for k, v in manufacturer_counts.items()])
    unique_floors = data['Floor'].nunique()
    unique_rooms = data['Room'].nunique()
    total_work_orders = data['Work Orders'].sum()
    total_repairs = data['Repairs'].sum()
    
    # Average operational time calculation
    current_date = datetime.now()
    data['Operational Time'] = (current_date - pd.to_datetime(data['Last Serviced Date'])).dt.days
    avg_operational_time = data['Operational Time'].mean()
    
    # Create the summary
    summary = f"""
    The building contains a total of {total_assets} assets. 
    The assets are distributed among types as: {asset_type_summary}.
    They are manufactured by: {manufacturer_summary}.
    These assets are spread across {unique_floors} unique floors and {unique_rooms} unique rooms.
    The total work orders and repairs for these assets amount to {total_work_orders} and {total_repairs} respectively.
    The average operational time of the assets is approximately {avg_operational_time:.2f} days.
    """
    return summary

# Main chatbot function
def chat_with_gpt3_and_dataset(user_query):
    context = detailed_summarize_dataset()
    combined_input = context + "\n\nUser: " + user_query + "\nAssistant:"
    
    # Get the response from GPT-3.5-Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a natural language interface for a dataset meant to answer the user's questions with data from the dataset, and make predictions from the data when asked."},
            {"role": "user", "content": combined_input}
        ]
    )
    return response.choices[0].message['content'].strip()

# CLI interaction loop
def main():
    print("GPT-3.5-Turbo Chatbot with CBRE Dataset Integration\n")
    print("Type 'exit' to end the chat.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            response = chat_with_gpt3_and_dataset(user_input)
            print("Chatbot: ", response)

if __name__ == "__main__":
    main()
