import yfinance as yf
import pandas as pd
from datetime import datetime


def check_breakout(ticker, lookback_days=35, volume_multiplier=1.5, start="2015-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    data = yf.download(ticker, start=start, end=end, progress=False)
    if data.empty:
        return {"ticker": ticker, "error": "No data found"}
    data.columns = data.columns.get_level_values(0)
    data = data.dropna()

    if len(data) < lookback_days + 1:
        return {"ticker": ticker, "error": "Not enough data"}

    recent_high = data["High"].iloc[-lookback_days:].max()
    current_price = data["Close"].iloc[-1]
    current_volume = data["Volume"].iloc[-1]
    avg_volume = data["Volume"].iloc[-lookback_days:-1].mean()

    is_new_high = current_price >= recent_high * 0.99
    volume_confirmed = current_volume >= avg_volume * volume_multiplier

    if is_new_high and volume_confirmed:
        signal = "BREAKOUT DETECTED"
        reason = f"Price near {lookback_days}-day high, volume {round(current_volume/avg_volume, 2)}x average"
    else:
        signal = "No signal"
        reasons = []
        if not is_new_high:
            reasons.append(f"Not at {lookback_days}-day high")
        if not volume_confirmed:
            reasons.append(f"Volume not confirmed ({round(current_volume/avg_volume, 2)}x average, need {volume_multiplier}x)")
        reason = "; ".join(reasons)

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "recent_high": round(recent_high, 2),
        "volume_ratio": round(current_volume / avg_volume, 2),
        "signal": signal,
        "reason": reason,
    }


def check_near_breakout(ticker, lookback_days=20, proximity_pct=5, start="2025-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    data = yf.download(ticker, start=start, end=end, progress=False)
    if data.empty:
        return {"ticker": ticker, "error": "No data found"}
    data.columns = data.columns.get_level_values(0)
    data = data.dropna()

    if len(data) < lookback_days + 1:
        return {"ticker": ticker, "error": "Not enough data"}

    recent_high = data["High"].iloc[-lookback_days:-1].max()
    current_price = data["Close"].iloc[-1]

    distance_pct = (recent_high - current_price) / recent_high * 100

    if 0 < distance_pct <= proximity_pct:
        signal = "NEAR BREAKOUT"
        reason = f"Only {round(distance_pct, 2)}% below {lookback_days}-day high of {round(recent_high, 2)}"
    elif current_price > recent_high:
        signal = "Already broke out"
        reason = "Price already above recent high — check Breakout signal instead"
    else:
        signal = "No signal"
        reason = f"{round(distance_pct, 2)}% below {lookback_days}-day high — not close enough yet"

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "recent_high": round(recent_high, 2),
        "distance_pct": round(distance_pct, 2),
        "signal": signal,
        "reason": reason,
    }


if __name__ == "__main__":
    print(check_breakout("LOTUSDEV.NS"))
    print(check_near_breakout("LOTUSDEV.NS"))