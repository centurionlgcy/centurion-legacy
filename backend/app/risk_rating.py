def calculate_risk(df):
    last = df.iloc[-1]
    atr = last["atr"]
    avg_atr = df["atr"].rolling(20).mean().iloc[-1]

    ratio = atr / avg_atr

    if ratio > 1.5:
        return "High"

    if ratio > 0.8:
        return "Medium"

    return "Low"

