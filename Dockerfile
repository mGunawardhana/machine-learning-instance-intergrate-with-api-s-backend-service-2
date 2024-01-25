# Docker base image.
FROM python:3.10.12

# Working directory inside the container.
WORKDIR /code

# Copy the requirements.txt inside the image.
COPY ./requirements.txt /code/requirements.txt

# Install project dependencies.
RUN pip install -v --no-cache-dir --upgrade -r /code/requirements.txt

# Copy project files to the image.
COPY . /code

# Run the contianer - force port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]