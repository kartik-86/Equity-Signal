import yfinance as yf


def fundamental_score(ticker):
    try:
        info = yf.Ticker(ticker).info

        revenue_growth = info.get("revenueGrowth")
        profit_margin = info.get("profitMargins")
        debt_equity = info.get("debtToEquity")
        insider_holding = info.get("heldPercentInsiders")
        sector = info.get("sector", "Unknown")

        score = 0
        breakdown = {}

        if revenue_growth is None:
            g = 0
        elif revenue_growth >= 0.5:
            g = 30
        elif revenue_growth >= 0.2:
            g = 22
        elif revenue_growth >= 0:
            g = 12
        else:
            g = 0
        score += g
        breakdown["growth_score"] = g

        if profit_margin is None:
            p = 0
        elif profit_margin >= 0.15:
            p = 30
        elif profit_margin >= 0.05:
            p = 20
        elif profit_margin >= 0:
            p = 8
        else:
            p = 0
        score += p
        breakdown["profitability_score"] = p

        if debt_equity is None:
            d = 12
        elif debt_equity <= 20:
            d = 25
        elif debt_equity <= 50:
            d = 18
        elif debt_equity <= 100:
            d = 10
        else:
            d = 3
        score += d
        breakdown["financial_health_score"] = d

        if insider_holding is None:
            i = 5
        elif insider_holding >= 0.5:
            i = 15
        elif insider_holding >= 0.2:
            i = 10
        else:
            i = 4
        score += i
        breakdown["insider_score"] = i

        note = ""
        if sector == "Financial Services":
            note = "Financial sector — debt/equity comparison not meaningful (lenders carry high leverage by design)"

        return {
            "ticker": ticker,
            "sector": sector,
            "fundamental_score": score,
            **breakdown,
            "revenue_growth": revenue_growth,
            "profit_margin": profit_margin,
            "debt_to_equity": debt_equity,
            "insider_holding": insider_holding,
            "note": note,
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


if __name__ == "__main__":
    print(fundamental_score("TEMPSENS.NS"))