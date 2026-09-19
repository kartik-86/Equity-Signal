const tickerNames = {
    "TEMPSENS.NS": "Tempsens Instruments",
    "HONASA.NS": "Honasa Consumer",
    "CELLO.NS": "Cello World",
    "IREDA.NS": "IREDA",
    "JIOFIN.NS": "Jio Financial Services",
    "GROWW.NS": "Groww",
    "PWL.NS": "Physics Wallah",
    "URBANCO.NS": "Urban Company",
    "ARDEE.NS": "Ardee Engineering",
    "BLEL.NS": "Behari Lal Engineering",
    "SHANKESH.NS": "Shankesh Jewellers",
    "TURTLEMINT.NS": "Turtlemint",
    "LGEINDIA.NS": "LG Electronics India",
    "SBIFUNDS.NS": "SBI Funds Management",
    "PRIORITY.NS": "Priority Jewels",
    "SHIPROCKET.NS": "Shiprocket",
    "LOTUSDEV.NS": "Sri Lotus Developers",
    "KUSUMGAR.NS": "Kusumgar Corporates",
    "SAILIFE.NS": "Sai Life Sciences",
    "WAAREEENER.NS": "Waaree Energies",
    "VMM.NS": "Vishal Mega Mart",
    "TATACAP.NS": "Tata Capital",
    "BHARATCOAL.NS": "Bharat Coking Coal",
    "COALINDIA.NS": "Coal India",
    "TATASTEEL.NS": "Tata Steel",
    "ATHERENERG.NS": "Ather Energy",
    "VEDL.NS": "Vedanta",
    "POWERGRID.NS": "Power Grid Corporation",
    "IRFC.NS": "IRFC",
    "BEL.NS": "Bharat Electronics",
    "SBIN.NS": "State Bank of India",
    "HDFCBANK.NS": "HDFC Bank",
    "BIRET.NS": "Brookfield India REIT",
    "EMBASSY.NS": "Embassy Office Parks REIT",
    "TATAGOLD.NS": "Tata Gold ETF",
    "KRT.BO": "Knowledge Realty Trust",
    "ESDS.NS": "ESDS Software Solutions",
    "TAPARIA.BO": "Taparia Tools"
};

function displayName(ticker) {
    return tickerNames[ticker] || ticker;
}

function buildCandleField() {
    const field = document.getElementById("candleField");
    if (!field) return;
    field.innerHTML = "";

    const count = 70;
    const tealIndices = [48, 56, 64];
    const redIndices = [52, 60];

    for (let i = 0; i < count; i++) {
        const bar = document.createElement("div");

        if (tealIndices.includes(i)) {
            const height = 60 + Math.random() * 30;
            bar.className = "candle candle-signal-teal";
            bar.style.height = height + "%";
            bar.style.animationDelay = (tealIndices.indexOf(i) * 0.5) + "s";
        } else if (redIndices.includes(i)) {
            const height = 30 + Math.random() * 15;
            bar.className = "candle candle-signal-red";
            bar.style.height = height + "%";
            bar.style.animationDelay = (redIndices.indexOf(i) * 0.6) + "s";
        } else {
            const isUp = Math.random() > 0.45;
            const height = 20 + Math.random() * 70;
            bar.className = "candle " + (isUp ? "candle-up" : "candle-down");
            bar.style.height = height + "%";
        }

        field.appendChild(bar);
    }
}

buildCandleField();

const strategiesMeta = {
    recovery: {
        title: "IPO Recovery",
        desc: "Identifies newly listed stocks that fell from an early high and are genuinely climbing back toward it.",
        endpoint: "/dashboard",
        signal: "SETUP DETECTED"
    },
    breakout: {
        title: "Breakout",
        desc: "Flags stocks making fresh highs on unusually strong volume, right now.",
        endpoint: "/dashboard/breakout",
        signal: "BREAKOUT DETECTED"
    },
    near: {
        title: "Near Breakout",
        desc: "Watchlist of stocks approaching resistance, not there yet but close.",
        endpoint: "/dashboard/near-breakout",
        signal: "NEAR BREAKOUT"
    }
};

const allPages = ["home", "strategies", "strategy-detail", "mystocks", "ai", "about", "alerts"];

function showPage(page) {
    allPages.forEach(p => {
        const el = document.getElementById(`page-${p}`);
        if (el) el.style.display = p === page ? "block" : "none";
    });

    document.getElementById("nav-home").classList.toggle("active", page === "home");
    document.getElementById("nav-strategies").classList.toggle("active", page === "strategies" || page === "strategy-detail");
    document.getElementById("nav-mystocks").classList.toggle("active", page === "mystocks");
    document.getElementById("nav-ai").classList.toggle("active", page === "ai");
    document.getElementById("nav-about").classList.toggle("active", page === "about");
    document.getElementById("nav-alerts").classList.toggle("active", page === "alerts");

    if (page === "strategies") {
        loadStrategiesOverview();
    }
    if (page === "mystocks") {
        loadMyStocks();
    }
}

async function loadStrategiesOverview() {
    for (const key of Object.keys(strategiesMeta)) {
        const meta = strategiesMeta[key];
        const response = await fetch(`http://127.0.0.1:8000${meta.endpoint}`);
        const data = await response.json();
        const matches = data.filter(s => s.signal === meta.signal).length;
        document.getElementById(`count-${key}`).textContent =
            `${matches} stock${matches === 1 ? "" : "s"} matching`;
    }
}

function signalBadge(signal) {
    if (["SETUP DETECTED", "BREAKOUT DETECTED"].includes(signal)) {
        return `<span class="signal-badge signal-good">${signal}</span>`;
    }
    if (signal === "NEAR BREAKOUT") {
        return `<span class="signal-badge signal-watch">${signal}</span>`;
    }
    return `<span class="signal-none">${signal || "N/A"}</span>`;
}

function renderStockCard(stock, key) {
    let metrics = "";

    if (key === "recovery") {
        metrics = `
            <div class="stock-metric"><span>Drawdown</span><strong>${stock.drawdown_pct ?? "-"}%</strong></div>
            <div class="stock-metric"><span>Retracement</span><strong>${stock.retracement_pct ?? "-"}%</strong></div>
        `;
    } else if (key === "breakout") {
        metrics = `
            <div class="stock-metric"><span>Current price</span><strong>₹${stock.current_price ?? "-"}</strong></div>
            <div class="stock-metric"><span>20-day high</span><strong>₹${stock.recent_high ?? "-"}</strong></div>
            <div class="stock-metric"><span>Volume ratio</span><strong>${stock.volume_ratio ?? "-"}x</strong></div>
        `;
    } else {
        metrics = `
            <div class="stock-metric"><span>Current price</span><strong>₹${stock.current_price ?? "-"}</strong></div>
            <div class="stock-metric"><span>Recent high</span><strong>₹${stock.recent_high ?? "-"}</strong></div>
            <div class="stock-metric"><span>Distance</span><strong>${stock.distance_pct ?? "-"}%</strong></div>
        `;
    }

    const fundId = `fund-${stock.ticker.replace(".", "-")}`;

    return `
        <div class="stock-card">
            <div class="stock-card-head">
                <div>
                    <div class="stock-name">${displayName(stock.ticker)}</div>
                    <div class="stock-ticker-sub">${stock.ticker}</div>
                </div>
                ${signalBadge(stock.signal)}
            </div>
            <button class="watchlist-btn" onclick="addToWatchlist('${stock.ticker}')">+ Watchlist</button>
            ${metrics}
            <div class="stock-metric" id="${fundId}"><span>Fundamental score</span><strong>Loading…</strong></div>
            <div class="stock-reason">${stock.reason || stock.error || ""}</div>
        </div>
    `;
}

async function openStrategy(key) {
    showPage("strategy-detail");
    const meta = strategiesMeta[key];

    document.getElementById("detail-title").textContent = meta.title;
    document.getElementById("detail-desc").textContent = meta.desc;

    const response = await fetch(`http://127.0.0.1:8000${meta.endpoint}`);
    const data = await response.json();
    const matches = data.filter(s => s.signal === meta.signal);

    const grid = document.getElementById("stockGrid");
    const empty = document.getElementById("detailEmptyState");

    if (matches.length === 0) {
        grid.innerHTML = "";
        empty.style.display = "block";
        return;
    }

    empty.style.display = "none";
    grid.innerHTML = matches.map(stock => renderStockCard(stock, key)).join("");

    matches.forEach(async (stock) => {
        const fundResponse = await fetch(`http://127.0.0.1:8000/fundamentals/${stock.ticker}`);
        const fund = await fundResponse.json();
        const el = document.getElementById(`fund-${stock.ticker.replace(".", "-")}`);
        if (el && fund.fundamental_score !== undefined) {
            el.innerHTML = `
                <span>Fundamental score</span>
                <strong class="${fund.fundamental_score >= 55 ? 'score-good' : 'score-weak'}">${fund.fundamental_score}/100</strong>
            `;
        } else if (el) {
            el.innerHTML = `<span>Fundamental score</span><strong>N/A</strong>`;
        }
    });
}

function getWatchlist() {
    const saved = localStorage.getItem("watchlist");
    return saved ? JSON.parse(saved) : [];
}

function saveWatchlist(list) {
    localStorage.setItem("watchlist", JSON.stringify(list));
}

function addToWatchlist(ticker) {
    const list = getWatchlist();
    if (!list.includes(ticker)) {
        list.push(ticker);
        saveWatchlist(list);
    }
    alert(`${ticker} added to My Stocks`);
}

function removeFromWatchlist(ticker) {
    const list = getWatchlist().filter(t => t !== ticker);
    saveWatchlist(list);
    loadMyStocks();
}

async function addManualTicker() {
    const input = document.getElementById("manualTickerInput");
    const ticker = input.value.trim().toUpperCase();
    if (!ticker) return;
    addToWatchlist(ticker);
    input.value = "";
    loadMyStocks();
}

function renderWatchlistCard(overview, isBase) {
    const { ticker, recovery, breakout, near_breakout, fundamentals } = overview;

    const signals = [];
    if (recovery.signal === "SETUP DETECTED") signals.push(signalBadge("SETUP DETECTED"));
    if (breakout.signal === "BREAKOUT DETECTED") signals.push(signalBadge("BREAKOUT DETECTED"));
    if (near_breakout.signal === "NEAR BREAKOUT") signals.push(signalBadge("NEAR BREAKOUT"));
    const signalHtml = signals.length ? signals.join(" ") : `<span class="signal-none">No active signal</span>`;

    const fundScore = fundamentals.fundamental_score !== undefined
        ? `${fundamentals.fundamental_score}/100`
        : "N/A";

    const removeBtn = isBase ? "" : `<button class="remove-btn" onclick="removeFromWatchlist('${ticker}')">Remove</button>`;

    return `
        <div class="stock-card">
            <div class="stock-card-head">
                <div>
                    <div class="stock-name">${displayName(ticker)}</div>
                    <div class="stock-ticker-sub">${ticker}</div>
                </div>
                ${removeBtn}
            </div>
            <div class="stock-metric"><span>Signals</span><span>${signalHtml}</span></div>
            <div class="stock-metric"><span>Fundamental score</span><strong>${fundScore}</strong></div>
        </div>
    `;
}

let baseTickers = [];

async function loadMyStocks() {
    const grid = document.getElementById("watchlistGrid");
    const empty = document.getElementById("watchlistEmptyState");

    if (baseTickers.length === 0) {
        const res = await fetch("http://127.0.0.1:8000/tickers/all");
        const data = await res.json();
        baseTickers = data.tickers;
    }

    const extra = getWatchlist().filter(t => !baseTickers.includes(t));
    const fullList = [...baseTickers, ...extra];

    if (fullList.length === 0) {
        grid.innerHTML = "";
        empty.style.display = "block";
        return;
    }
    empty.style.display = "none";
    grid.innerHTML = fullList.map(() => `<div class="stock-card">Loading…</div>`).join("");

    const overviews = await Promise.all(
        fullList.map(t => fetch(`http://127.0.0.1:8000/stock/${t}`).then(r => r.json()))
    );

    grid.innerHTML = overviews.map(o => renderWatchlistCard(o, baseTickers.includes(o.ticker))).join("");
}