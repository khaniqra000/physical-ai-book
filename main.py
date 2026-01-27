
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Physical AI Backend is Running!", "database": "Neon Connected"}

@app.get("/ask")
def ask_ai(question: str):
    # Yeh hissa baad mein chatbot se connect hoga
    return {"answer": f"Aapne poocha: {question}. Main jaldi hi iska jawab doonga!"}