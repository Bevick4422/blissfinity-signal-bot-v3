import asyncio

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
bearish_pullback
)

from telegram_sender import send_signal

from trade_tracker import (
main as run_tracker
)

========================================
MARKET SCANNER
========================================

async def scan_market():

print("\n========================")
print("BLISSFINITY V3")
print("========================\n")

signals_sent = 0

for pair in SYMBOLS:

    if signals_sent >= MAX_SIGNALS:
        break

    print(f"Scanning {pair}...")

    try:

        trend_df, bos_df, entry_df = get_market_data(

            pair,
            TREND_TIMEFRAME,
            BOS_TIMEFRAME,
            ENTRY_TIMEFRAME

        )

        if (
            trend_df is None
            or bos_df is None
            or entry_df is None
        ):

            print(
                f"{pair} -> missing timeframe data"
            )

            continue

        # ====================================
        # LONG
        # ====================================

        if (

            bullish_trend(trend_df)

            and

            bullish_bos(bos_df)

            and

            bullish_pullback(entry_df)

        ):

            entry = round(
                float(
                    entry_df["close"].iloc[-1]
                ),
                4
            )

            stoploss = round(
                entry * 0.985,
                4
            )

            tp1 = round(
                entry * 1.03,
                4
            )

            tp2 = round(
                entry * 1.06,
                4
            )

            await send_signal(

                pair,
                "LONG",
                entry,
                stoploss,
                tp1,
                tp2

            )

            print(
                f"{pair} LONG SENT"
            )

            signals_sent += 1

        # ====================================
        # SHORT
        # ====================================

        elif (

            bearish_trend(trend_df)

            and

            bearish_bos(bos_df)

            and

            bearish_pullback(entry_df)

        ):

            entry = round(
                float(
                    entry_df["close"].iloc[-1]
                ),
                4
            )

            stoploss = round(
                entry * 1.015,
                4
            )

            tp1 = round(
                entry * 0.97,
                4
            )

            tp2 = round(
                entry * 0.94,
                4
            )

            await send_signal(

                pair,
                "SHORT",
                entry,
                stoploss,
                tp1,
                tp2

            )

            print(
                f"{pair} SHORT SENT"
            )

            signals_sent += 1

        else:

            print(
                f"{pair} -> no setup"
            )

        await asyncio.sleep(1)

    except Exception as e:

        print(
            f"{pair} scan error:"
        )

        print(e)

print("\n========================")
print("SCAN COMPLETE")
print("========================\n")
========================================
MASTER LOOP
========================================

async def main():

while True:

    try:

        await scan_market()

        try:

            await run_tracker()

        except Exception as e:

            print(
                f"Tracker Error: {e}"
            )

        print(
            "\nSleeping 5 minutes...\n"
        )

        await asyncio.sleep(300)

    except Exception as e:

        print(
            f"Bot Error: {e}"
        )

        await asyncio.sleep(60)
========================================
START
========================================

if name == "main":

asyncio.run(main())