from fastapi.middleware.cors import CORSMiddleware

import ccxt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
allow_origins=["https://crypto-arbitrage-frontend.vercel.app"]

app.add_middleware(CORSMiddleware, allow_origins=["*"])

kucoin = ccxt.kucoin()
binance_futures = ccxt.binance({'options': {'defaultType': 'future'}})
symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "BNB/USDT"]

@app.get("/futures-vs-spot")
def compare():
    data = []
    for symbol in symbols:
        future_price = binance_futures.fetch_ticker(symbol)['last']
        spot_price = kucoin.fetch_ticker(symbol)['last']
        diff = future_price - spot_price
        percent = (diff / spot_price) * 100
        data.append({
            "symbol": symbol,
            "futures_price": future_price,
            "spot_price": spot_price,
            "diff": diff,
            "percent": percent
        })
    return data
