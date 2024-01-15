import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = pd.read_csv("uber.csv")
data["Date/Time"] = data["Date/Time"].map(pd.to_datetime)

@app.get("/")
async def root():
    return {"message": "Hello from Uber Trip Analysing Backend"}

@app.get("/data")
async def get_first_five_rows_in_dataset():
    return {"message": data.head().to_dict(orient="records")}

data["Day"] = data["Date/Time"].apply(lambda x: x.day)
data["Weekday"] = data["Date/Time"].apply(lambda x: x.weekday())
data["Hour"] = data["Date/Time"].apply(lambda x: x.hour)

@app.get("/level-one/optimised/data")
async def get_level_one_type_optimised_data():
    return {"message": data.head().to_dict(orient="records")}

@app.get("/level-one/optimised/data/visualise/day")
async def get_level_one_type_optimised_data_visualise_day():
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Day"])
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()
    
    return {"image_data": img_str}

@app.get("/level-one/optimised/data/visualise/hour")
async def get_level_one_type_optimised_data_visualise_hour():
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Hour"])
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()
    
    return {"image_data": img_str}

@app.get("/level-one/optimised/data/visualise/weekday")
async def get_level_one_type_optimised_data_visualise_weekday():
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Weekday"])
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()
    
    return {"image_data": img_str}

@app.get("/level-one/optimised/data/visualise/bubble-map")
async def get_level_one_type_optimised_data_visualise_bubble_map():
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x="Lon", y="Lat", hue="Day", size="Day")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    return {"image_data": img_str}

