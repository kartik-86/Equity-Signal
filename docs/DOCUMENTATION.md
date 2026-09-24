# Equity Signal — Project Documentation

## What this is

Equity Signal is a rule-based market intelligence tool for Indian equities. It checks a
tracked list of ~37 stocks against three strategies, shows results on a live dashboard, and
sends Telegram alerts on a match. Live at https://equity-signal.onrender.com/app — shared
privately (self + one friend), not public.

**Disclaimer:** Research and decision-support tool, not investment advice. Investments in the
securities market are subject to market risks.

---

## Architecture

yfinance (data)
↓
backend/app/strategies/ → strategy + fundamental logic
↓
backend/app/main.py → FastAPI, exposes logic as endpoints, serves the frontend
↓
backend/app/static/ → single-page frontend
↓
backend/app/alerts/ → checks strategies, sends Telegram alert


Strategy logic lives only in `strategies/`, imported by both the API and the alert script —
one place for the actual rules.

**Stack:** Python, FastAPI, yfinance, plain HTML/CSS/JS (no framework — deliberate choice,
avoids a second toolchain for a small site), Telegram Bot API, Render (hosting, free tier).

---

## Strategy 1: IPO Recovery

Looks for a stock that had a strong post-listing peak, fell meaningfully from it, and is now
genuinely climbing back — not just any dip, a real recovery pattern. Measures the fall
(drawdown) and how much of that fall has been climbed back (retracement), and flags a setup
when both are in a sensible range. Only applies to recently listed stocks — running it on old,
established companies produces meaningless numbers, since it's anchored to a stock's very
first trading days.

**Status:** partially backtested only — 5 completed test trades, mixed/weak results (40% win
rate). Not statistically reliable yet. Treat any current signal as "worth watching," not
"proven to work."

## Strategy 2 & 3: Breakout / Near Breakout

Looks for a stock making a fresh price high on unusually strong trading volume — a sign of
real, aggressive buying interest, not just quiet drifting. "Near Breakout" is a softer
watch-list version: close to that fresh high, not there yet. Works for any stock, new or old.

**Status:** detection logic tested and confirmed working on real examples. Not backtested for
actual profitability — no built-in entry/exit or stop-loss logic; it only detects and alerts.

## Fundamental Scoring

A separate 0-100 score (growth, profitability, debt level, insider ownership) shown alongside
every signal, for context only — it never hides or filters a signal. Known limitation: the
data source doesn't provide standard profitability metrics for Indian stocks, so a substitute
is used, and debt-level scoring isn't meaningful for banks/lenders (flagged, not corrected).

---

## Deployment

Hosted on Render (free tier), auto-deploys from GitHub on every push to `main`. Free tier
sleeps after 15 minutes idle — first visit after that takes 20-60 seconds to wake up.

---

## Running locally

```powershell
conda activate equity-signal
uvicorn backend.app.main:app --reload
```
Visit `http://127.0.0.1:8000/app`

Run alerts manually:
```powershell
python backend/app/alerts/run_alerts.py
```

---

## Known limitations, honestly

- Strategies not rigorously backtested — treat signals as informative, not proven.
- Tracked stock list is hand-picked, not a full market scan.
- No database — every check re-fetches live data.
- Alerts run manually, not yet scheduled.
- No login system — watchlist is per-browser only.
- Shared privately only, given the above.