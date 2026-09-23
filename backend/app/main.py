from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import sys
import os

sys.path.append(os.path.dirname(__file__))

from strategies.ipo_recovery import check_signal
from strategies.breakout import check_breakout, check_near_breakout
from strategies.fundamentals import fundamental_score

app = FastAPI()

recovery_tickers = [
    "TEMPSENS.NS", "HONASA.NS", "CELLO.NS", "IREDA.NS", "JIOFIN.NS",
    "GROWW.NS", "PWL.NS", "URBANCO.NS", "ARDEE.NS", "BLEL.NS",
    "SHANKESH.NS", "TURTLEMINT.NS", "LGEINDIA.NS", "SBIFUNDS.NS",
    "PRIORITY.NS", "SHIPROCKET.NS", "LOTUSDEV.NS", "KUSUMGAR.NS",
    "SAILIFE.NS", "WAAREEENER.NS", "VMM.NS"
]

breakout_tickers = recovery_tickers + [
    "TATACAP.NS", "BHARATCOAL.NS", "COALINDIA.NS", "TATASTEEL.NS",
    "ATHERENERG.NS", "VEDL.NS", "POWERGRID.NS", "IRFC.NS",
    "BEL.NS", "SBIN.NS", "HDFCBANK.NS", "BIRET.NS",
    "EMBASSY.NS", "TATAGOLD.NS", "KRT.BO", "ESDS.NS", "TAPARIA.BO"
]


@app.get("/")
def home():
    return RedirectResponse(url="/app")


@app.get("/signal/{ticker}")
def get_signal(ticker: str):
    return check_signal(ticker)


@app.get("/dashboard")
def get_dashboard():
    return [check_signal(t) for t in recovery_tickers]


@app.get("/breakout/{ticker}")
def get_breakout(ticker: str):
    return check_breakout(ticker)


@app.get("/dashboard/breakout")
def get_breakout_dashboard():
    return [check_breakout(t) for t in breakout_tickers]


@app.get("/near-breakout/{ticker}")
def get_near_breakout(ticker: str):
    return check_near_breakout(ticker)


@app.get("/dashboard/near-breakout")
def get_near_breakout_dashboard():
    return [check_near_breakout(t) for t in breakout_tickers]


app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

@app.get("/fundamentals/{ticker}")
def get_fundamentals(ticker: str):
    return fundamental_score(ticker)

@app.get("/stock/{ticker}")
def get_stock_overview(ticker: str):
    return {
        "ticker": ticker,
        "recovery": check_signal(ticker),
        "breakout": check_breakout(ticker),
        "near_breakout": check_near_breakout(ticker),
        "fundamentals": fundamental_score(ticker),
    }

@app.get("/tickers/all")
def get_all_tickers():
    combined = sorted(set(recovery_tickers) | set(breakout_tickers))
    return {"tickers": combined}


@app.get("/app")
def serve_frontend():
    return FileResponse("backend/app/static/index.html")