import pandas as pd 
from enum import Enum

# enum class which contains actions
class ClientActions(str, Enum):
    purchase = 'purchase'
    add_to_cart = 'add_to_cart'
    view_product = 'view_product'

# load data from csv file
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# aggregate data by client_id
def aggregate_client_actions(data):
    actions = data.groupby('client_id').size().reset_index(name='number_of_actions')
    return actions

# filtering data by client actions
def filter_client_action(data, client_action: str):
    actions = data[data['action'] == client_action]
    return actions

# function to return average actions and active clients
def analyze_client_behavior(data):
    # using mean to calculate average actions made by clients
    average_actions = data.groupby('client_id').size().mean()
    # using pandas sort values function to return top 5 active clients
    client_with_most_actions = aggregate_client_actions(data).sort_values(by='number_of_actions', ascending=False).head(2)
    return average_actions, client_with_most_actions

# saving aggregate data to csv file
def save_processed_data(data, output_file):
    try:
        # saving data in csv format
        data.to_csv(output_file)
        return True
    # checking for permission access
    except PermissionError:
        print("User don't have access to save file in this Path:", output_file)
        return False
