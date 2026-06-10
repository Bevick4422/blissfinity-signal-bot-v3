from telegram import Bot

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)

import json
import os
from datetime import datetime

# ========================================
# TELEGRAM
# ========================================

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN missing")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID missing")

bot = Bot(
    token=TELEGRAM_TOKEN.strip()
)

# ========================================
# ACTIVE TRADES FILE
# ========================================

ACTIVE_TRADES_FILE = "active_trades.json"

# ========================================
# LOAD TRADES
# ========================================

def load_trades():

    try:

        if not os.path.exists(
            ACTIVE_TRADES_FILE
        ):
            return []

        with open(
            ACTIVE_TRADES_FILE,
            "r"
        ) as f:

            data = json.load(f)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:

        print(
            f"Trade load error: {e}"
        )

        return []

# ========================================
# SAVE TRADES
# ========================================

def save_trades(trades):

    try:

        with open(
            ACTIVE_TRADES_FILE,
            "w"
        ) as f:

            json.dump(
                trades,
                f,
                indent=4
            )

    except Exception as e:

        print(
            f"Trade save error: {e}"
        )

# ========================================
# SAVE SINGLE TRADE
# ========================================

def save_trade(trade):

    trades = load_trades()

    trades.append(trade)

    save_trades(trades)

# ========================================
# SEND SIGNAL
# ========================================

async def send_signal(
    pair,
    direction,
    entry,
    stoploss,
    tp1,
    tp2
):

    try:

        message = (
            f"🚨 BLISSFINITY V2\n\n"
            f"Pair: {pair}\n\n"
            f"Direction: {direction}\n\n"
            f"Entry: {entry}\n\n"
            f"Stop Loss: {stoploss}\n\n"
            f"TP1: {tp1}\n\n"
            f"TP2: {tp2}"
        )

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )

        print(
            f"{pair} {direction} signal sent."
        )

        trade = {

            "pair": pair,
            "direction": direction,

            "entry": float(entry),

            "sl": float(stoploss),

            "tp1": float(tp1),

            "tp2": float(tp2),

            "status": "OPEN",

            "tp1_hit": False,

            "tp2_hit": False,

            "opened_at": str(
                datetime.utcnow()
            )
        }

        save_trade(trade)

    except Exception as e:

        print(
            f"Telegram error: {e}"
        )

# ========================================
# SEND GENERAL MESSAGE
# ========================================

async def send_message(text):

    try:

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text
        )

    except Exception as e:

        print(
            f"Telegram message error: {e}"
        )