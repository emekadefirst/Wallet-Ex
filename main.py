from fastapi import FastAPI
from auth.routes import auth
from wallet.route import wallet
from auth.verify import validate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse

class Edit(BaseModel):
    message: str 

app = FastAPI(
    title="Expendier Wallet API",
    description="Well this Project demonstrate the use of Submub API",
    version="0.0.1"
)


app.include_router(auth, prefix="/auth")
app.include_router(validate, prefix="/validatae")
app.include_router(wallet, prefix="/wallet")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the Expendier Wallet API"}


