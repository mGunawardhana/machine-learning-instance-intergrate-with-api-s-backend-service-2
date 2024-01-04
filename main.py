import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fastapi import FastAPI

app = FastAPI()

data = pd.read_csv("uber.csv")

# The following line of code is used to convert the "Date/Time" column of the dataframe 'data' into datetime format.
# The 'map' function is used to apply the 'pd.to_datetime' function to each element in the "Date/Time" column.
# 'pd.to_datetime' is a pandas function that converts a string or an array-like object into a datetime object.
# After this line of code is executed, the "Date/Time" column will contain datetime objects instead of strings.
data["Date/Time"] = data["Date/Time"].map(pd.to_datetime)


@app.get("/")
async def root():
    return {"message": "Hello from Uber Trip Analysing Backend"}


@app.get("/data")
async def get_first_five_rows_in_dataset():
    return {"message": data.head()}


# The following line of code is creating a new column in the dataframe `data` named "Day".
# This column is populated by applying a lambda function to each element in the "Date/Time" column.
# The lambda function `lambda x: x.day` extracts the day from the datetime object `x`.
# As a result, the "Day" column will contain the day of the month for each corresponding datetime in the "Date/Time" column.
data["Day"] = data["Date/Time"].apply(lambda x: x.day)

# The following line of code is creating a new column in the dataframe `data` named "Weekday".
# This column is populated by applying a lambda function to each element in the "Date/Time" column.
# The lambda function `lambda x: x.weekday()` extracts the weekday from the datetime object `x`.
# As a result, the "Weekday" column will contain the weekday for each corresponding datetime in the "Date/Time" column.
# The weekday is an integer, where Monday is 0 and Sunday is 6.
data["Weekday"] = data["Date/Time"].apply(lambda x: x.weekday())

# The following line of code is creating a new column in the dataframe `data` named "Hour".
# This column is populated by applying a lambda function to each element in the "Date/Time" column.
# The lambda function `lambda x: x.hour` extracts the hour from the datetime object `x`.
# As a result, the "Hour" column will contain the hour for each corresponding datetime in the "Date/Time" column.
# The hour is an integer, where 0 represents midnight and 23 represents 11 PM.
data["Hour"] = data["Date/Time"].apply(lambda x: x.hour)


@app.get("/level-one/optimised/data")
async def get_level_one_type_optimised_data():
    return {"message": data.head()}


sns.set(rc={'figure.figsize': (12, 10)})


@app.get("/level-one/optimised/data/visualise/day")
async def get_level_one_type_optimised_data_visualise_day():
    return {"message": sns.histplot(data["Day"])}


@app.get("/level-one/optimised/data/visualise/hour")
async def get_level_one_type_optimised_data_visualise_hour():
    return {"message": sns.histplot(data["Hour"])}


@app.get("/level-one/optimised/data/visualise/weekday")
async def get_level_one_type_optimised_data_visualise_weekday():
    return {"message": sns.histplot(data["Weekday"])}


# we can't show this diagram
df = data.groupby(["Weekday", "Hour"]).apply(lambda x: len(x))
df = df.unstack()
sns.heatmap(df, annot=False)

# The following line of code is creating a scatter plot using the 'plot' function of the pandas dataframe 'data'.
# The 'kind' parameter is set to 'scatter' to specify that a scatter plot should be created.
# The 'x' and 'y' parameters are set to 'Lon' and 'Lat', respectively, to specify that these columns of the dataframe should be used as the x and y coordinates of the scatter plot.
# The 'alpha' parameter is set to 0.4 to specify the transparency of the points in the scatter plot.
# The 's' parameter is set to 'data['Day']' to specify the size of the points in the scatter plot. This means that the size of the points will correspond to the day of the month.
# The 'label' parameter is set to 'Uber Trips' to specify the label for the data in the scatter plot.
# The 'figsize' parameter is set to (12, 8) to specify the size of the figure in inches.
# The 'cmap' parameter is set to 'plt.get_cmap('jet')' to specify the colormap for the scatter plot. The 'jet' colormap is a popular colormap that ranges from blue to red.
data.plot(kind='scatter', x='Lon', y='Lat', alpha=0.4, s=data['Day'], label='Uber Trips', figsize=(12, 8),
          cmap=plt.get_cmap('jet'))

plt.title("Uber Trips Analysis")

# The following line of code is used to add a legend to the scatter plot.
# The 'legend' function of matplotlib's pyplot module ('plt') is used to create the legend.
# The legend uses the 'label' parameter that was set in the 'plot' function to create the labels for the data in the scatter plot.
# The legend helps in identifying the different data points in the scatter plot.
plt.legend()

# The following line of code is used to display all the figures and plots that have been created in the script.
# The 'show' function of matplotlib's pyplot module ('plt') is used to display the figures.
# This function should be called after all the figures and plots have been created and all the necessary settings have been applied.
# This function does not take any parameters.
# After this function is called, the figures and plots will be displayed in a new window.
plt.show()


@app.get("/level-one/optimised/data/visualise/bubble-map")
async def get_level_one_type_optimised_data_visualise_bubble_map():
    return {"message": sns.scatterplot(data["Lon"], data["Lat"], hue=data["Day"], size=data["Day"])}
