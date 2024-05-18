from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from .utils import (ClientActions,
                   load_data, 
                   aggregate_client_actions, 
                   filter_client_action, 
                   analyze_client_behavior,
                   save_processed_data,)

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # using temporary file to save data
    with open("temp.csv", "wb") as f:
        f.write(await file.read())
    
    # Load the data from the temporary file
    data = load_data("temp.csv")
    

    aggregated_data = aggregate_client_actions(data)
    average_actions, top_5_clients = analyze_client_behavior(data)
    
    # Removing temporary file
    os.remove("temp.csv")
    
    # using pandas to_dict function, where orient="records" returns list like value
    response = {
        "average_actions": average_actions,
        "top_5_clients": top_5_clients.to_dict(orient="records"),
        "aggregated_data": aggregated_data.to_dict(orient="records")
    }
    return response


# function saves data to upload file
@app.post("/save/")
async def save_data(file: UploadFile = File(...)):
    # using temporary file to save data
    with open("temp.csv", "wb") as f:
        f.write(await file.read())
    
    # Load the data from the temporary file
    data = load_data("temp.csv")
    
    aggregated_data = aggregate_client_actions(data)
    
    # Removing temporary file
    os.remove("temp.csv")
    save_data = os.path.join('uploads\saved_data.csv')
    
    # check for data correctness, and return correct HttpResponse 
    if save_processed_data(aggregated_data, save_data):
        return HTTPException(status_code=200, detail='File saved successfully')
    else:
        return HTTPException(status_code=400, detail='File not saved successfully')
    

# function filtres client action 
@app.post("/filter/")
async def filter_data(client_action: ClientActions, file: UploadFile = File(...)):\
    # using temporary file to save data
    with open("temp.csv", "wb") as f:
        f.write(await file.read())
    
    # Load the data from the temporary file
    data = load_data("temp.csv")
    
    filtered_data = filter_client_action(data, client_action)
    # Removing temporary file
    os.remove("temp.csv")
    return filtered_data.to_dict(orient="records")
