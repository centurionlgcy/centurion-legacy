import ta

def apply_indicators(df, ema_fast, ema_slow, rsi_period, atr_period):
    df["ema_fast"] = ta.trend.EMAIndicator(df["close"], ema_fast).ema_indicator()
    df["ema_slow"] = ta.trend.EMAIndicator(df["close"], ema_slow).ema_indicator()
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], rsi_period).rsi()
    df["atr"] = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"], atr_period).average_true_range()

    df.dropna(inplace=True)
    return df
