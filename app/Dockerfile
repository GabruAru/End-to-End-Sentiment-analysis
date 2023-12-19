# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt


ENV DATABASE_URL=mysql+mysqlconnector://root:admin@db/sentiment
ENV MODEL_FILE_PATH=/app/ai_model/model/roberta_sentiment    

CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]

