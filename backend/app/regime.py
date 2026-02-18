import ta

def detect_regime(df):
    df["adx"] = ta.trend.ADXIndicator(
        df["high"], df["low"], df["close"], 14
    ).adx()

    last = df.iloc[-1]

    if last["adx"] > 25:
        return "Trending"

    return "Ranging"

