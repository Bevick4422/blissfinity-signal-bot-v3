import pandas as pd


# =====================================
# TREND
# =====================================

def bullish_trend(df):

    try:

        ema20 = df["close"].rolling(20).mean()

        return (
            df["close"].iloc[-1]
            > ema20.iloc[-1]
        )

    except:
        return False


def bearish_trend(df):

    try:

        ema20 = df["close"].rolling(20).mean()

        return (
            df["close"].iloc[-1]
            < ema20.iloc[-1]
        )

    except:
        return False


# =====================================
# BREAK OF STRUCTURE
# =====================================

def bullish_bos(df):

    try:

        last_close = df["close"].iloc[-1]

        previous_high = (
            df["high"]
            .iloc[-20:-1]
            .max()
        )

        return last_close > previous_high

    except:
        return False


def bearish_bos(df):

    try:

        last_close = df["close"].iloc[-1]

        previous_low = (
            df["low"]
            .iloc[-20:-1]
            .min()
        )

        return last_close < previous_low

    except:
        return False


# =====================================
# PULLBACK ENTRY
# =====================================

def bullish_pullback(df):

    try:

        close = df["close"].iloc[-1]
        low = df["low"].iloc[-5:].min()

        return close > low

    except:
        return False


def bearish_pullback(df):

    try:

        close = df["close"].iloc[-1]
        high = df["high"].iloc[-5:].max()

        return close < high

    except:
        return False


# =====================================
# SUPPLY / DEMAND FILTER
# =====================================

def near_demand(df):

    try:

        current = df["close"].iloc[-1]

        demand = (
            df["low"]
            .iloc[-30:]
            .min()
        )

        distance = abs(current - demand) / current

        return distance <= 0.02

    except:
        return False


def near_supply(df):

    try:

        current = df["close"].iloc[-1]

        supply = (
            df["high"]
            .iloc[-30:]
            .max()
        )

        distance = abs(current - supply) / current

        return distance <= 0.02

    except:
        return False