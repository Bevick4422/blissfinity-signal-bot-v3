python
import asyncio
import json
import os

from config import (
    SYMBOLS,
    MAX_SIGNALS,
    TREND_TIMEFRAME,
    BOS_TIMEFRAME,
    ENTRY_TIMEFRAME
)

from scanner import get_market_data

from signal_engine import (
    bullish_trend,
    bearish_trend,
    bullish_bos,
    bearish_bos,
    bullish_pullback,
    bearish_pullback,
    near_demand,
    near_supply
)

from telegram_sender import send_signal

from trade_tracker import main as run_tracker

SIGNAL_FILE = "signals.json"

# ========================
# SIGNAL STORAGE
# ========================

def load_signals():
    if not os.path.exists(SIGNAL_FILE):
        return {}

    try:
        with open(SIGNAL_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_signals(data):
    with open(SIGNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ========================
# MARKET SCAN
# ========================

async def scan_market():

    print("\n========================")
    print("BLISSFINITY V3")
    print("========================\n")

    signal_history = load_signals()
    signals_sent = 0

    for pair in SYMBOLS:

        if signals_sent >= MAX_SIGNALS:
            break

        print(f"Scanning {pair}...")

        trend_df, bos_df, entry_df = get_market_data(
            pair,
            TREND_TIMEFRAME,
            BOS_TIMEFRAME,
            ENTRY_TIMEFRAME
        )

        if trend_df is None or bos_df is None or entry_df is None:
            continue

        long_setup = (
            bullish_trend(trend_df)
            and bullish_bos(bos_df)
            and bullish_pullback(entry_df)
            and near_demand(entry_df)
        )

        short_setup = (
            bearish_trend(trend_df)
            and bearish_bos(bos_df)
            and bearish_pullback(entry_df)
            and near_supply(entry_df)
        )

        # LONG
        if long_setup:

            if signal_history.get(pair) == "LONG":
                continue

            entry = round(float(entry_df["close"].iloc[-1]), 4)
            stoploss = round(entry * 0.98, 4)
            tp1 = round(entry * 1.03, 4)
            tp2 = round(entry * 1.06, 4)

            await send_signal(pair, "LONG", entry, stoploss, tp1, tp2)

            signal_history[pair] = "LONG"
            signals_sent += 1

            print(f"{pair} LONG SENT")

        # SHORT
        elif short_setup:

            if signal_history.get(pair) == "SHORT":
                continue

            entry = round(float(entry_df["close"].iloc[-1]), 4)
            stoploss = round(entry * 1.02, 4)
            tp1 = round(entry * 0.97, 4)
            tp2 = round(entry * 0.94, 4)

            await send_signal(pair, "SHORT", entry, stoploss, tp1, tp2)

            signal_history[pair] = "SHORT"
            signals_sent += 1

            print(f"{pair} SHORT SENT")

        else:
            signal_history[pair] = "NONE"

        await asyncio.sleep(1)

    save_signals(signal_history)

    print("\n========================")
    print("SCAN COMPLETE")
    print("========================\n")


# ========================
# MAIN LOOP
# ========================

async def main():

    while True:

        try:
            await scan_market()

            try:
                await run_tracker()
            except Exception as e:
                print(f"Tracker Error: {e}")

            print("\nSleeping 5 Minutes...\n")
            await asyncio.sleep(300)

        except Exception as e:
            print(f"Bot Error: {e}")
            await asyncio.sleep(60)


# ========================
# START
# ========================

if __name__ == "__main__":
    asyncio.run(main())