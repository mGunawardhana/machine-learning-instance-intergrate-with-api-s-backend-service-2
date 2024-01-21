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

# Extract day, weekday, and hour information from the timestamp
data["Day"] = data["Date/Time"].apply(lambda x: x.day)
data["Weekday"] = data["Date/Time"].apply(lambda x: x.weekday())
data["Hour"] = data["Date/Time"].apply(lambda x: x.hour)


@app.get("/")
async def root():
    return {"message": "Hello from Uber Trip Analyzing Backend"}


@app.get("/data")
async def get_first_five_rows_in_dataset():
    return {"message": data.head().to_dict(orient="records")}


@app.get("/level-one/optimised/data")
async def get_level_one_type_optimised_data():
    return {"message": data.head().to_dict(orient="records")}


@app.get("/level-one/optimised/data/visualise/day")
async def get_level_one_type_optimised_data_visualise_day():
    # Create a histogram for the distribution of trips across days
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Day"])
    plt.title("Distribution of Uber Trips Across Days")
    plt.xlabel("Day of the Month")
    plt.ylabel("Number of Trips")

    # Save the plot as a PNG image and encode it in base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    # Return the encoded image data
    return {"image_data": img_str}


@app.get("/level-one/optimised/data/visualise/hour")
async def get_level_one_type_optimised_data_visualise_hour():
    # Create a histogram for the distribution of trips across hours
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Hour"])
    plt.title("Distribution of Uber Trips Across Hours")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Trips")

    # Save the plot as a PNG image and encode it in base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    # Return the encoded image data
    return {"image_data": img_str}


@app.get("/level-one/optimised/data/visualise/weekday")
async def get_level_one_type_optimised_data_visualise_weekday():
    # Create a histogram for the distribution of trips across weekdays
    plt.figure(figsize=(8, 6))
    sns.histplot(data["Weekday"])
    plt.title("Distribution of Uber Trips Across Weekdays")
    plt.xlabel("Weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)")
    plt.ylabel("Number of Trips")

    # Save the plot as a PNG image and encode it in base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    # Return the encoded image data
    return {"image_data": img_str}


@app.get("/level-one/optimised/data/visualise/bubble-map")
async def get_level_one_type_optimised_data_visualise_bubble_map():
    # Create a scatter plot with a bubble map representation
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x="Lon", y="Lat", hue="Day", size="Day", palette="viridis", alpha=0.7)
    plt.title("Geographical Distribution of Uber Trips with Day-wise Bubbles")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save the plot as a PNG image and encode it in base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    # Return the encoded image data
    return {"image_data": img_str}
