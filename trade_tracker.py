import json
import requests
import asyncio

from telegram_sender import send_message

ACTIVE_TRADES_FILE = "active_trades.json"


def load_trades():

    try:

        with open(
            ACTIVE_TRADES_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return []


def save_trades(trades):

    with open(
        ACTIVE_TRADES_FILE,
        "w"
    ) as f:

        json.dump(
            trades,
            f,
            indent=4
        )


def get_price(symbol):

    try:

        url = (
            f"https://contract.mexc.com"
            f"/api/v1/contract/ticker"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        for item in data["data"]:

            if item["symbol"] == symbol:

                return float(
                    item["lastPrice"]
                )

    except Exception as e:

        print(e)

    return None


async def check_trade(trade):

    price = get_price(
        trade["pair"]
    )

    if price is None:

        return trade

    direction = trade["direction"]

    # LONG TRADES

    if direction == "LONG":

        if (
            not trade["tp1_hit"]
            and price >= trade["tp1"]
        ):

            await send_message(

                f"🎯 TP1 HIT\n\n"
                f"{trade['pair']}\n"
                f"LONG\n\n"
                f"Entry: {trade['entry']}\n"
                f"TP1: {trade['tp1']}"
            )

            trade["tp1_hit"] = True

        if price >= trade["tp2"]:

            await send_message(

                f"🚀 TP2 HIT\n\n"
                f"{trade['pair']}\n"
                f"LONG CLOSED"
            )

            trade["status"] = "CLOSED"

        elif price <= trade["sl"]:

            await send_message(

                f"❌ STOP LOSS HIT\n\n"
                f"{trade['pair']}\n"
                f"LONG CLOSED"
            )

            trade["status"] = "CLOSED"

    # SHORT TRADES

    elif direction == "SHORT":

        if (
            not trade["tp1_hit"]
            and price <= trade["tp1"]
        ):

            await send_message(

                f"🎯 TP1 HIT\n\n"
                f"{trade['pair']}\n"
                f"SHORT\n\n"
                f"Entry: {trade['entry']}\n"
                f"TP1: {trade['tp1']}"
            )

            trade["tp1_hit"] = True

        if price <= trade["tp2"]:

            await send_message(

                f"🚀 TP2 HIT\n\n"
                f"{trade['pair']}\n"
                f"SHORT CLOSED"
            )

            trade["status"] = "CLOSED"

        elif price >= trade["sl"]:

            await send_message(

                f"❌ STOP LOSS HIT\n\n"
                f"{trade['pair']}\n"
                f"SHORT CLOSED"
            )

            trade["status"] = "CLOSED"

    return trade


async def main():

    print(
        "\n========================"
    )

    print(
        "TRACKING TRADES"
    )

    print(
        "========================\n"
    )

    trades = load_trades()

    updated = []

    for trade in trades:

        if trade["status"] == "OPEN":

            trade = await check_trade(
                trade
            )

        updated.append(
            trade
        )

    save_trades(updated)

    print(
        "Tracking completed.\n"
    )


if __name__ == "__main__":

    asyncio.run(main())