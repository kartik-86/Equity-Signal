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





tracked_tickers = [
    "TEMPSENS.NS", "HONASA.NS", "CELLO.NS", "IREDA.NS", "JIOFIN.NS",
    "GROWW.NS", "PWL.NS", "URBANCO.NS", "ARDEE.NS", "BLEL.NS",
    "SHANKESH.NS", "TURTLEMINT.NS", "LGEINDIA.NS", "SBIFUNDS.NS",
    "PRIORITY.NS", "SHIPROCKET.NS", "LOTUSDEV.NS", "KUSUMGAR.NS",
    "SAILIFE.NS", "WAAREEENER.NS", "VMM.NS"
]


@app.get("/dashboard")
def get_dashboard():
    return [check_signal(t) for t in tracked_tickers]




from strategies.breakout import check_breakout


@app.get("/breakout/{ticker}")
def get_breakout(ticker: str):
    return check_breakout(ticker)


@app.get("/dashboard/breakout")
def get_breakout_dashboard():
    return [check_breakout(t) for t in tracked_tickers]