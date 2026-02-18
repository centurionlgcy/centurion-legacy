from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.data import fetch_ohlcv
from app.indicators import apply_indicators
from app.signals import generate_signal
from app.logger import log_signal
from app.performance import calculate_performance
from app.config import (
    SYMBOLS,
    CONFIRMATION_TIMEFRAME,
    EMA_FAST,
    EMA_SLOW,
    RSI_PERIOD,
    ATR_PERIOD,
    RISK_REWARD,
    API_KEYS
)

app = FastAPI(
    title="Centurion Legacy™ Elite Signals API",
    description="""
Institutional-grade AI-powered market signals.
""",
    version="1.0.0"
)

# ✅ CORS middleware (correct placement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Centurion Legacy API Running"}

@app.get("/signals")
def get_signals(api_key: str = Query(...)):

    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    plan = API_KEYS[api_key]
    results = {}

    for asset in SYMBOLS:

        df_primary = fetch_ohlcv(asset["symbol"], asset["timeframe"])
        df_primary = apply_indicators(df_primary, EMA_FAST, EMA_SLOW, RSI_PERIOD, ATR_PERIOD)

        signal = generate_signal(df_primary, RISK_REWARD)

        threshold = 65 if plan == "PREMIUM" else 55

        signal["confidence"] = max(0, min(signal["confidence"], 95))

        if signal["confidence"] < threshold:
            signal["signal"] = "NO TRADE"
            signal["stop_loss"] = None
            signal["take_profit"] = None
            signal["risk_reward"] = None

        if signal["confidence"] >= 80:
            signal["signal_strength"] = "Strong"
        elif signal["confidence"] >= 60:
            signal["signal_strength"] = "Moderate"
        else:
            signal["signal_strength"] = "Weak"

        log_signal(asset["symbol"], plan, signal)

        results[asset["symbol"]] = {
            "plan": plan,
            "market": asset["market"],
            "timeframe": asset["timeframe"],
            **signal
        }

    return results

@app.get("/performance")
def get_performance(api_key: str = Query(...)):

    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return calculate_performance()
