import requests
import pandas as pd

# ========================================

# MEXC TIMEFRAME MAP

# ========================================

TIMEFRAME_MAP = {


"Min1": "Min1",
"Min5": "Min5",
"Min15": "Min15",
"Min30": "Min30",
"Min60": "Min60",

"Hour4": "Hour4",
"Hour8": "Hour8",

"Day1": "Day1"


}

# ========================================

# GET KLINES

# ========================================

def get_klines(
symbol,
timeframe,
limit=200
):


try:

    interval = TIMEFRAME_MAP.get(
        timeframe
    )

    if not interval:

        print(
            f"{symbol} invalid timeframe: {timeframe}"
        )

        return None

    url = (
        f"https://contract.mexc.com"
        f"/api/v1/contract/kline/{symbol}"
        f"?interval={interval}"
    )

    response = requests.get(
        url,
        timeout=15
    )

    if response.status_code != 200:

        print(
            f"{symbol} HTTP {response.status_code}"
        )

        return None

    data = response.json()

    if data.get("success") is False:

        print(
            f"{symbol} API ERROR"
        )

        print(data)

        return None

    candles = data.get("data")

    if not candles:

        print(
            f"{symbol} no candles"
        )

        return None

    df = pd.DataFrame({

        "open": candles["open"],
        "high": candles["high"],
        "low": candles["low"],
        "close": candles["close"]

    })

    df = df.astype(float)

    if len(df) < 50:

        print(
            f"{symbol} insufficient candles"
        )

        return None

    return df.tail(limit)

except Exception as e:

    print(
        f"{symbol} scanner error:"
    )

    print(e)

    return None


# ========================================

# MULTI TIMEFRAME DATA

# ========================================

def get_market_data(


symbol,

trend_tf,

bos_tf,

entry_tf
```

):


trend_df = get_klines(

    symbol,
    trend_tf

)

bos_df = get_klines(

    symbol,
    bos_tf

)

entry_df = get_klines(

    symbol,
    entry_tf

)

if trend_df is None:

    return None, None, None

if bos_df is None:

    return None, None, None

if entry_df is None:

    return None, None, None

return (

    trend_df,
    bos_df,
    entry_df

)
