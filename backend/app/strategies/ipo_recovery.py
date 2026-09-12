import yfinance as yf
import pandas as pd


def analyze_ipo(ticker, start="2025-01-01", end="2026-09-11", reference_days=5, min_days_after=5):
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        if data.empty:
            return {"ticker": ticker, "error": "No data found"}

        data.columns = data.columns.get_level_values(0)

        if len(data) < reference_days + min_days_after:
            return {"ticker": ticker, "error": "Too new — not enough post-reference data yet"}

        ref_high = data["High"].iloc[:reference_days].max()
        lowest_after = data["Low"].iloc[reference_days:].min()
        drawdown = (ref_high - lowest_after) / ref_high * 100

        current_price = data["Close"].iloc[-1]
        recovery = current_price / ref_high * 100
        retracement = (current_price - lowest_after) / (ref_high - lowest_after) * 100

        return {
            "ticker": ticker,
            "reference_high": round(ref_high, 2),
            "lowest_after_high": round(lowest_after, 2),
            "drawdown_pct": round(drawdown, 2),
            "current_price": round(current_price, 2),
            "recovery_pct": round(recovery, 2),
            "retracement_pct": round(retracement, 2),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def check_signal(ticker, min_drawdown=15, min_retracement=65, max_retracement=110, reference_days=5):
    result = analyze_ipo(ticker, reference_days=reference_days)

    if "error" in result and result.get("drawdown_pct") is None:
        result["signal"] = "Not evaluated"
        result["reason"] = result["error"]
        return result

    drawdown_ok = result["drawdown_pct"] >= min_drawdown
    retracement_ok = min_retracement <= result["retracement_pct"] <= max_retracement

    if drawdown_ok and retracement_ok:
        result["signal"] = "SETUP DETECTED"
        result["reason"] = f"Drawdown {result['drawdown_pct']}% >= {min_drawdown}%, Retracement {result['retracement_pct']}% in [{min_retracement}-{max_retracement}]%"
    else:
        result["signal"] = "No signal"
        reasons = []
        if not drawdown_ok:
            reasons.append(f"Drawdown too small ({result['drawdown_pct']}% < {min_drawdown}%)")
        if not retracement_ok:
            if result["retracement_pct"] < min_retracement:
                reasons.append(f"Retracement too weak ({result['retracement_pct']}% < {min_retracement}%)")
            else:
                reasons.append(f"Already overshot old high ({result['retracement_pct']}% > {max_retracement}%) — past the entry window")
        result["reason"] = "; ".join(reasons)

    return result


def backtest_signal(ticker, reference_days=5, min_drawdown=15, min_retracement=65, max_retracement=110, holding_period=60, start="2025-01-01", end="2026-09-11"):
    data = yf.download(ticker, start=start, end=end, progress=False)
    if data.empty:
        return {"ticker": ticker, "error": "No data found"}
    data.columns = data.columns.get_level_values(0)

    if len(data) < reference_days + 1:
        return {"ticker": ticker, "error": "Not enough data"}

    ref_high = data["High"].iloc[:reference_days].max()

    signal_date = None
    signal_price = None
    signal_position = None

    for i in range(reference_days, len(data)):
        data_so_far = data.iloc[:i + 1]
        lowest_so_far = data_so_far["Low"].iloc[reference_days:].min()
        drawdown_so_far = (ref_high - lowest_so_far) / ref_high * 100
        price_today = data_so_far["Close"].iloc[-1]
        retracement_so_far = (price_today - lowest_so_far) / (ref_high - lowest_so_far) * 100

        if drawdown_so_far >= min_drawdown and min_retracement <= retracement_so_far <= max_retracement:
            signal_date = data_so_far.index[-1]
            signal_price = price_today
            signal_position = i
            break

    if signal_date is None:
        return {"ticker": ticker, "error": "No signal ever triggered in this period"}

    exit_position = signal_position + holding_period
    if exit_position >= len(data):
        return {"ticker": ticker, "signal_date": signal_date, "signal_price": round(signal_price, 2),
                "error": "Not enough days after signal to complete holding period yet"}

    exit_price = data["Close"].iloc[exit_position]
    exit_date = data.index[exit_position]
    return_pct = (exit_price - signal_price) / signal_price * 100

    return {
        "ticker": ticker,
        "signal_date": signal_date.date(),
        "signal_price": round(signal_price, 2),
        "exit_date": exit_date.date(),
        "exit_price": round(exit_price, 2),
        "return_pct": round(return_pct, 2),
    }


if __name__ == "__main__":
    result = check_signal("TEMPSENS.NS")
    print(result)