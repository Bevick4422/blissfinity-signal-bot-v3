import os

# ========================================
# TELEGRAM
# ========================================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

# ========================================
# TIMEFRAMES
# ========================================

TREND_TIMEFRAME = "Hour4"
BOS_TIMEFRAME = "Min60"
ENTRY_TIMEFRAME = "Min15"
# ========================================
# SIGNAL SETTINGS
# ========================================

MAX_SIGNALS = 4

# ========================================
# WATCHLIST
# ========================================

SYMBOLS = [

    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XRP_USDT",
    "DOGE_USDT",

    "AVAX_USDT",
    "LINK_USDT",
    "ADA_USDT",
    "SUI_USDT",
    "WLD_USDT",

    "NEAR_USDT",
    "INJ_USDT",
    "SEI_USDT",
    "TIA_USDT",

    "ARB_USDT",
    "OP_USDT",
    "APT_USDT",
    "ATOM_USDT",
    "TRX_USDT",

    "ICP_USDT",
    "HBAR_USDT",
    "FET_USDT",
    "RUNE_USDT",
    "PENDLE_USDT"

]