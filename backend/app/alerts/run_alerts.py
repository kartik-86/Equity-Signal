import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from strategies.ipo_recovery import check_signal
from strategies.breakout import check_breakout, check_near_breakout
from alerts.telegram_alert import send_telegram_alert

tracked_tickers = [
    "TEMPSENS.NS", "HONASA.NS", "CELLO.NS", "IREDA.NS", "JIOFIN.NS",
    "GROWW.NS", "PWL.NS", "URBANCO.NS", "ARDEE.NS", "BLEL.NS",
    "SHANKESH.NS", "TURTLEMINT.NS", "LGEINDIA.NS", "SBIFUNDS.NS",
    "PRIORITY.NS", "SHIPROCKET.NS", "LOTUSDEV.NS", "KUSUMGAR.NS",
    "SAILIFE.NS", "WAAREEENER.NS", "VMM.NS"
]


def run_all_checks():
    messages = []

    for ticker in tracked_tickers:
        recovery = check_signal(ticker)
        if recovery.get("signal") == "SETUP DETECTED":
            messages.append(f"🟢 *{ticker}* — IPO Recovery Setup\n{recovery['reason']}")

        breakout = check_breakout(ticker)
        if breakout.get("signal") == "BREAKOUT DETECTED":
            messages.append(f"🚀 *{ticker}* — Breakout Detected\n{breakout['reason']}")

        near = check_near_breakout(ticker)
        if near.get("signal") == "NEAR BREAKOUT":
            messages.append(f"👀 *{ticker}* — Near Breakout\n{near['reason']}")

    if messages:
        full_message = "📊 *Equity Signal — Daily Alerts*\n\n" + "\n\n".join(messages)
    else:
        full_message = "📊 *Equity Signal* — No signals matched today."

    send_telegram_alert(full_message)
    print(full_message)


if __name__ == "__main__":
    run_all_checks()