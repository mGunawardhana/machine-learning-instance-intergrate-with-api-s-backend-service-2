from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    data = pd.read_csv("uber.csv")
    data["Date/Time"] = pd.to_datetime(data["Date/Time"])
    data["Day"] = data["Date/Time"].dt.day
    data["Weekday"] = data["Date/Time"].dt.weekday
    data["Hour"] = data["Date/Time"].dt.hour
except Exception as e:
    logger.error(f"Error loading data: {str(e)}")
    raise SystemExit(1)

def save_and_encode_plot(figure, filename, max_val, min_val):
    try:
        img_buffer = BytesIO()
        figure.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        return {"image_data": img_str, "max_val": int(max_val.item()), "min_val": int(min_val.item())}
    except Exception as e:
        logger.error(f"Error saving/encoding plot {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello from Root End-Point!"}

@app.get("/level-one/optimised/data")
async def get_level_one_type_optimised_data():
    logger.info("Get data endpoint accessed")
    return {"message": data.head().to_dict(orient="records")}

@app.get("/level-one/optimised/data/visualise/day")
async def get_level_one_type_optimised_data_visualise_day():
    try:
        plt.figure(figsize=(8, 6))
        sns.histplot(data["Day"])
        plt.title("Distribution of Uber Trips Across Days")
        plt.xlabel("Day of the Month")
        plt.ylabel("Number of Trips")
        # plt.text(10, 1000, "This chart shows the distribution of Uber trips across different days of the month. The x-axis represents the day of the month and the y-axis represents the number of trips. The height of the bars indicates the number of trips made on that particular day.")
        max_val = data["Day"].max()
        min_val = data["Day"].min()
        return save_and_encode_plot(plt, "visualise_day", max_val, min_val)
    except Exception as exception:
        logger.error(f"Error in visualize day endpoint: {str(exception)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/level-one/optimised/data/visualise/hour")
async def get_level_one_type_optimised_data_visualise_hour():
    try:
        plt.figure(figsize=(8, 6))
        sns.histplot(data["Hour"])
        plt.title("Distribution of Uber Trips Across Hours")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Number of Trips")
        max_val = data["Hour"].max()
        min_val = data["Hour"].min()
        return save_and_encode_plot(plt, "visualise_hour", max_val, min_val)
    except Exception as exception:
        logger.error(f"Error in visualize hour endpoint: {str(exception)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/level-one/optimised/data/visualise/weekday")
async def get_level_one_type_optimised_data_visualise_weekday():
    try:
        plt.figure(figsize=(8, 6))
        sns.histplot(data["Weekday"])
        plt.title("Distribution of Uber Trips Across Weekdays")
        plt.xlabel("Weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)")
        plt.ylabel("Number of Trips")
        max_val = data["Weekday"].max()
        min_val = data["Weekday"].min()
        return save_and_encode_plot(plt, "visualise_weekday", max_val, min_val)
    except Exception as exception:
        logger.error(f"Error in visualize weekday endpoint: {str(exception)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/level-one/optimised/data/visualise/bubble-map")
async def get_level_one_type_optimised_data_visualise_bubble_map():
    try:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=data, x="Lon", y="Lat", hue="Day", size="Day", palette="viridis", alpha=0.7)
        plt.title("Geographical Distribution of Uber Trips with Day-wise Bubbles")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        # plt.text(-73.9, 40.7, "This chart shows the geographical distribution of Uber trips with day-wise bubbles. The x-axis represents the longitude and the y-axis represents the latitude. The size and color of the bubbles indicate the day of the month.")
        max_val = data["Day"].max()
        min_val = data["Day"].min()
        return save_and_encode_plot(plt, "visualise_bubble_map", max_val, min_val)
    except Exception as exception:
        logger.error(f"Error in visualize bubble map endpoint: {str(exception)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")