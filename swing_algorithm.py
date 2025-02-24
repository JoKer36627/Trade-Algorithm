import ccxt
from dotenv import load_dotenv
import os

load_dotenv()

exchange = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('SECRET_KEY'),
    'enableRateLimit': True,
})

def find_swing_low_entry(prices, volumes, symbol='ETH/USDT', pip_offset=10, amount=0.01):
    if len(prices) < 3 or len(volumes) != len(prices):
        return None,

    avg_volume = sum(volumes) / len(volumes)
    print(f"Medium volume: {avg_volume}")
    print(f"Prices (last 20): {prices}")
    print(f"Volumes (last 20): {volumes}")

    for i in range(1, len(prices) - 1):
        if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
            if volumes[i] > avg_volume * 1.1:
                swing_low = prices[i]
                entry_price = swing_low + pip_offset
                print(f"A swing low has been found: {swing_low} | Volume: {volumes[i]} ETH")
                print(f"Entry point: {entry_price}")
                try:
                    order = exchange.create_limit_buy_order(symbol, amount, entry_price)
                    print(f"The limit order is placed: {amount} {symbol} for {entry_price}")
                    return entry_price, None
                except Exception as e:
                    return entry_price, f"Error when placing an order: {str(e)}"
    return None, "Swing low with imbalance not found"

def fetch_recent_data(symbol='ETH/USDT', timeframe='15m', limit=200):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        close_prices = [candle[4] for candle in ohlcv]
        volumes = [candle[5] for candle in ohlcv]
        return close_prices[-20:], volumes[-20:]
    except Exception as e:
        print(f"Data retrieval error: {str(e)}")
        return None, None

if __name__ == "__main__":
    symbol = 'ETH/USDT'
    pip_offset = 10
    amount = 0.01

    real_prices, real_volumes = fetch_recent_data(symbol, '15m', 30)
    if real_prices:

        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        print(f"Current price: {current_price}")

        entry_price, error = find_swing_low_entry(
            real_prices, real_volumes, symbol=symbol, pip_offset=pip_offset, amount=amount
        )
        if entry_price:
            print(f"Successful: Entry point for {symbol} = {entry_price}")
        else:
            print(f"Error: {error}")
    else:
        print("Failed to retrieve data from the exchange")