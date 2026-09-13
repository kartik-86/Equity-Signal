from fastapi import FastAPI
import sys
import os

# Allow importing from the strategies folder
sys.path.append(os.path.dirname(__file__))

from strategies.ipo_recovery import check_signal

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Equity Signal API is running"}


@app.get("/signal/{ticker}")
def get_signal(ticker: str):
    return check_signal(ticker)






from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")


@app.get("/app")
def serve_frontend():
    return FileResponse("backend/app/static/index.html")