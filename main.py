from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="Expendier Wallet API",
    description="Well this Project demonstrate the use of Submub API",
    version="0.0.1"
)

@app.get("/")
def home():
    return {"message": "Welcome to the Expendier Wallet API"}
