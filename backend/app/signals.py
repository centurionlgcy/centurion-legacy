from app.regime import detect_regime
from app.risk_rating import calculate_risk

MIN_VOLATILITY_PERCENT = 0.10

def generate_signal(df, risk_reward):
    regime = detect_regime(df)
    risk = calculate_risk(df)
    last = df.iloc[-1]

    ema_fast = last["ema_fast"]
    ema_slow = last["ema_slow"]
    rsi = last["rsi"]
    atr = last["atr"]
    entry = last["close"]

    trend_strength = abs(ema_fast - ema_slow) / entry * 100
    volatility_percent = atr / entry * 100

    confidence = 50

    if ema_fast > ema_slow:
        confidence += 15
        direction = "BUY"
    elif ema_fast < ema_slow:
        confidence += 15
        direction = "SELL"
    else:
        direction = "NO TRADE"

    if 45 < rsi < 55:
        confidence += 5
    elif rsi < 40 or rsi > 60:
        confidence += 10

    if trend_strength > 0.8:
        confidence += 10

    # Volatility filter (light)
    if volatility_percent < MIN_VOLATILITY_PERCENT:
        direction = "NO TRADE"
        confidence -= 5

    confidence = max(0, min(confidence, 95))

    if confidence >= 80:
        strength = "Strong"
    elif confidence >= 60:
        strength = "Moderate"
    else:
        strength = "Weak"

    if direction == "BUY":
        stop = entry - atr
        take = entry + (entry - stop) * risk_reward
    elif direction == "SELL":
        stop = entry + atr
        take = entry - (stop - entry) * risk_reward
    else:
        stop = None
        take = None

    return {
        "signal": direction,
        "confidence": confidence,
        "signal_strength": strength,
        "trend_strength": round(trend_strength, 3),
        "volatility_percent": round(volatility_percent, 3),
        "entry": round(entry, 2),
        "stop_loss": round(stop, 2) if stop else None,
        "take_profit": round(take, 2) if take else None,
        "risk_reward": risk_reward if direction != "NO TRADE" else None,
        "regime": regime,
        "risk_rating": risk
    }
