from fastapi import FastAPI, UploadFile, File
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

