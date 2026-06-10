import pandas as pd

# =====================================
# TREND FILTER (4H)
# =====================================

def bullish_trend(df):

    try:

        ema20 = (
            df["close"]
            .rolling(20)
            .mean()
        )

        current = df["close"].iloc[-1]

        return current > ema20.iloc[-1]

    except Exception as e:

        print(
            f"bullish_trend error: {e}"
        )

        return False


def bearish_trend(df):

    try:

        ema20 = (
            df["close"]
            .rolling(20)
            .mean()
        )

        current = df["close"].iloc[-1]

        return current < ema20.iloc[-1]

    except Exception as e:

        print(
            f"bearish_trend error: {e}"
        )

        return False


# =====================================
# BREAK OF STRUCTURE (1H)
# =====================================

def bullish_bos(df):

    try:

        current_close = df["close"].iloc[-1]

        previous_high = (
            df["high"]
            .iloc[-20:-1]
            .max()
        )

        return current_close > previous_high

    except Exception as e:

        print(
            f"bullish_bos error: {e}"
        )

        return False


def bearish_bos(df):

    try:

        current_close = df["close"].iloc[-1]

        previous_low = (
            df["low"]
            .iloc[-20:-1]
            .min()
        )

        return current_close < previous_low

    except Exception as e:

        print(
            f"bearish_bos error: {e}"
        )

        return False


# =====================================
# PULLBACK ENTRY (15M)
# =====================================

def bullish_pullback(df):

    try:

        current = df["close"].iloc[-1]

        recent_high = (
            df["high"]
            .iloc[-20:]
            .max()
        )

        pullback_zone = (
            recent_high * 0.98
        )

        return (
            current <= recent_high
            and current >= pullback_zone
        )

    except Exception as e:

        print(
            f"bullish_pullback error: {e}"
        )

        return False


def bearish_pullback(df):

    try:

        current = df["close"].iloc[-1]

        recent_low = (
            df["low"]
            .iloc[-20:]
            .min()
        )

        pullback_zone = (
            recent_low * 1.02
        )

        return (
            current >= recent_low
            and current <= pullback_zone
        )

    except Exception as e:

        print(
            f"bearish_pullback error: {e}"
        )

        return False


# =====================================
# DEMAND FILTER
# =====================================

def near_demand(df):

    try:

        current = df["close"].iloc[-1]

        demand = (
            df["low"]
            .iloc[-30:]
            .min()
        )

        distance = (
            abs(current - demand)
            / current
        )

        return distance <= 0.02

    except Exception as e:

        print(
            f"near_demand error: {e}"
        )

        return False


# =====================================
# SUPPLY FILTER
# =====================================

def near_supply(df):

    try:

        current = df["close"].iloc[-1]

        supply = (
            df["high"]
            .iloc[-30:]
            .max()
        )

        distance = (
            abs(current - supply)
            / current
        )

        return distance <= 0.02

    except Exception as e:

        print(
            f"near_supply error: {e}"
        )

        return False