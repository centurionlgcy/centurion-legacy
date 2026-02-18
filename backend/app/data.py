import requests
import pandas as pd

def fetch_ohlcv(symbol: str, interval: str, limit: int = 200):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "timestamp","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    df = df[["timestamp","open","high","low","close","volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    return df

