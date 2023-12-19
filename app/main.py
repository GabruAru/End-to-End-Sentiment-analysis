import os
from pathlib import Path
from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import mysql.connector
from datetime import datetime
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , SessionEvents

app = FastAPI()

# Declare the SQLAlchemy Base

Base = declarative_base()



# Define the environment variable for the model file path
current_directory = Path(__file__).resolve().parent
MODEL_FILE_PATH = os.getenv("MODEL_FILE_PATH", current_directory / "ai_model" / "model" / "roberta_sentiment")

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:12345@db/sentiment")

engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define the Log model
class Log(Base):
    __tablename__ = "sentiment_logs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(length=255))  # Specify the length for VARCHAR
    sentiment_class = Column(String(length=255))  # Specify the length for VARCHAR
    timestamp = Column(String(length=255))  # Specify the length for VARCHAR

class SentimentRequest(BaseModel):
    text: str
    
# Create tables
Base.metadata.create_all(bind=engine)


#Loading the model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base', max_length=4096)
model = RobertaForSequenceClassification.from_pretrained(MODEL_FILE_PATH)

#Model_pre
def prediction(text):
    encodings = tokenizer(text, truncation=True, padding=True, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**encodings)
        predicted_class = torch.argmax(outputs.logits, dim=1)

    i = predicted_class.item()

    if i == 0:
        sentiment_class = "negative"

    elif i == 1:
        sentiment_class = "neutral"

    elif i == 2:
        sentiment_class = "positive"

    return sentiment_class

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI endpoint to get prediction
@app.post("/predict")
def predict_sentiment(request: SentimentRequest):
    try:
        # Perform sentiment analysis
        sentiment_class = prediction(request.text)

        #
        db = SessionLocal()
        log_entry = Log(text=request.text, sentiment_class=sentiment_class, timestamp=datetime.now())
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        return {"sentiment_class": sentiment_class}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/")
def get_logs(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    logs = db.query(Log).offset(skip).limit(limit).all()
    return logs
