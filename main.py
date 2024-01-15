import pandas as pd
import seaborn as sns
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

data = pd.read_csv("uber.csv")

data["Date/Time"] = data["Date/Time"].map(pd.to_datetime)

data["Day"] = data["Date/Time"].apply(lambda x: x.day)
data["Weekday"] = data["Date/Time"].apply(lambda x: x.weekday())
data["Hour"] = data["Date/Time"].apply(lambda x: x.hour)

def plot_bubble_map():
    bubble_data = {
        "Lon": data["Lon"].tolist(),
        "Lat": data["Lat"].tolist(),
        "Day": data["Day"].tolist()
    }
    return bubble_data

def plot_histogram_day():
    histogram_data = {
        "Day": data["Day"].tolist(),
        "Frequency": data["Day"].value_counts().sort_index().tolist()
    }
    return histogram_data

def plot_histogram_hour():
    histogram_data = {
        "Hour": data["Hour"].tolist(),
        "Frequency": data["Hour"].value_counts().sort_index().tolist()
    }
    return histogram_data

def plot_histogram_weekday():
    histogram_data = {
        "Weekday": data["Weekday"].tolist(),
        "Frequency": data["Weekday"].value_counts().sort_index().tolist()
    }
    return histogram_data

async def run_in_threadpool(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)

@app.get("/")
async def root():
    return {"message": "Hello from Uber Trip Analysing Backend"}

@app.get("/data")
async def get_first_five_rows_in_dataset():
    return {"message": data.head().to_dict(orient='records')}

@app.get("/level-one/optimised/data")
async def get_level_one_type_optimised_data():
    return {"message": data.head().to_dict(orient='records')}

@app.get("/level-one/optimised/data/visualise/day")
async def get_level_one_type_optimised_data_visualise_day():
    json_data = await run_in_threadpool(plot_histogram_day)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/level-one/optimised/data/visualise/hour")
async def get_level_one_type_optimised_data_visualise_hour():
    json_data = await run_in_threadpool(plot_histogram_hour)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/level-one/optimised/data/visualise/weekday")
async def get_level_one_type_optimised_data_visualise_weekday():
    json_data = await run_in_threadpool(plot_histogram_weekday)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/level-one/optimised/data/visualise/bubble-map")
async def get_level_one_type_optimised_data_visualise_bubble_map():
    json_data = await run_in_threadpool(plot_bubble_map)
    return JSONResponse(content=json_data, status_code=200)
