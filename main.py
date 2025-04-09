from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import ccxt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация бирж
exchanges = {
    "binance_futures": ccxt.binance({"options": {"defaultType": "future"}}),
    "kucoin": ccxt.kucoin(),
    "okx": ccxt.okx(),
    "bybit": ccxt.bybit(),
    "bitget": ccxt.bitget(),
}

# Топ-50 криптовалют с 50 до 100 места
symbols = [
    "FTM/USDT", "GRT/USDT", "RPL/USDT", "KAVA/USDT", "LDO/USDT", "WOO/USDT", "IOTA/USDT",
    "KSM/USDT", "CSPR/USDT", "ENJ/USDT", "ZIL/USDT", "COMP/USDT", "SNX/USDT", "BAT/USDT", "LRC/USDT",
    "YFI/USDT", "ONE/USDT", "GLM/USDT", "DASH/USDT", "GMT/USDT", "FLUX/USDT", "ARDR/USDT", "RSR/USDT",
    "BAL/USDT", "REN/USDT", "API3/USDT", "SRM/USDT", "BNT/USDT", "BAND/USDT", "ONG/USDT", "TOMO/USDT",
    "CTSI/USDT", "SNT/USDT", "KNC/USDT", "KEY/USDT", "RAY/USDT", "CVC/USDT", "TRU/USDT", "CHR/USDT",
    "ANT/USDT", "DNT/USDT", "NMR/USDT", "MDT/USDT", "IDEX/USDT", "FIS/USDT", "ALPHA/USDT", "STMX/USDT",
    "LIT/USDT", "BOND/USDT"
]

@app.get("/compare")
def compare(
    base_exchange: str = Query("binance_futures"),
    compare_exchange: str = Query("kucoin")
):
    if base_exchange not in exchanges or compare_exchange not in exchanges:
        return {"error": "Invalid exchange name"}

    base = exchanges[base_exchange]
    compare = exchanges[compare_exchange]
    
    data = []
    for symbol in symbols:
        try:
            base_price = base.fetch_ticker(symbol)['last']
            compare_price = compare.fetch_ticker(symbol)['last']
            diff = base_price - compare_price
            percent = (diff / compare_price) * 100
            data.append({
                "symbol": symbol,
                "base_exchange": base_exchange,
                "compare_exchange": compare_exchange,
                "base_price": base_price,
                "compare_price": compare_price,
                "diff": diff,
                "percent": percent
            })
        except Exception as e:
            print(f"Ошибка по паре {symbol}: {e}")
    return data
