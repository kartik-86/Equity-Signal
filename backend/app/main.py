from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os

sys.path.append(os.path.dirname(__file__))

from strategies.ipo_recovery import check_signal
from strategies.breakout import check_breakout, check_near_breakout

app = FastAPI()

tracked_tickers = [
    "TEMPSENS.NS", "HONASA.NS", "CELLO.NS", "IREDA.NS", "JIOFIN.NS",
    "GROWW.NS", "PWL.NS", "URBANCO.NS", "ARDEE.NS", "BLEL.NS",
    "SHANKESH.NS", "TURTLEMINT.NS", "LGEINDIA.NS", "SBIFUNDS.NS",
    "PRIORITY.NS", "SHIPROCKET.NS", "LOTUSDEV.NS", "KUSUMGAR.NS",
    "SAILIFE.NS", "WAAREEENER.NS", "VMM.NS"
]


@app.get("/")
def home():
    return {"message": "Equity Signal API is running"}


@app.get("/signal/{ticker}")
def get_signal(ticker: str):
    return check_signal(ticker)


@app.get("/dashboard")
def get_dashboard():
    return [check_signal(t) for t in tracked_tickers]


@app.get("/breakout/{ticker}")
def get_breakout(ticker: str):
    return check_breakout(ticker)


@app.get("/dashboard/breakout")
def get_breakout_dashboard():
    return [check_breakout(t) for t in tracked_tickers]


@app.get("/near-breakout/{ticker}")
def get_near_breakout(ticker: str):
    return check_near_breakout(ticker)


@app.get("/dashboard/near-breakout")
def get_near_breakout_dashboard():
    return [check_near_breakout(t) for t in tracked_tickers]


app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")


@app.get("/app")
def serve_frontend():
    return FileResponse("backend/app/static/index.html")