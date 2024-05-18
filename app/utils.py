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

def aggregate_client_actions(data):
    actions = data.groupby('client_id').size().reset_index(name='number_of_actions')
    return actions
