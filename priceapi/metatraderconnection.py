import MetaTrader5 as mt5
from datetime import datetime

class metatrader:
    def __init__(self):
        self.initialized = False
        self.symbols = []
    def initialize(self):
        if not mt5.initialize():
            raise Exception(f"❌ Failed to initialize MetaTrader5 API: {mt5.last_error()}")
        self.initialized = True
        self.symbols = self.get_all_symbols()
    def timeframe(self,seconds:int):
        mapping = {
        60: mt5.TIMEFRAME_M1,
        300: mt5.TIMEFRAME_M5,
        900: mt5.TIMEFRAME_M15,
        1800: mt5.TIMEFRAME_M30,
        3600: mt5.TIMEFRAME_H1,
        14400: mt5.TIMEFRAME_H4,
        86400: mt5.TIMEFRAME_D1,
        604800: mt5.TIMEFRAME_W1,
        2592000: mt5.TIMEFRAME_MN1,
        }

        if seconds not in mapping:
            raise ValueError(f"Unsupported timeframe: {seconds} seconds. Supported: {list(mapping.keys())}")

        return mapping[seconds]


    def get_all_symbols(self):
        if not self.initialized:
            self.initialize()
        symbols = mt5.symbols_get()
        if symbols is None:
            raise Exception(f"❌ Failed to get symbols: {mt5.last_error()}")
        return [symbol.name for symbol in symbols]

    def symbol_info_tick(self, symbol):
        if not self.initialized:
            raise Exception("❌ Not connected to MetaTrader 5")
        if symbol not in self.symbols:
            raise Exception(f"❌ Symbol {symbol} not found in MetaTrader 5 symbols list")
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise Exception(f"❌ Failed to get tick info for {symbol}: {mt5.last_error()}")
        return tick

    def symbol_info_history(self, symbol, timeframe, count=1000):
        """
        Get historical candles for a symbol
        :param symbol: e.g., 'XAUUSD'
        :param timeframe: e.g., mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5
        :param count: number of candles to fetch
        :return: list of dicts [{time, open, high, low, close}, ...]
        """
        if not self.initialized:
            raise Exception("❌ Not connected to MetaTrader 5")
        if symbol not in self.symbols:
            raise Exception(f"❌ Symbol {symbol} not found in MetaTrader 5 symbols list")
        
        # Get historical rates
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            raise Exception(f"❌ Failed to get historical data for {symbol}: {mt5.last_error()}")

        # Format data for API response
        candles = []
        for rate in rates:
            candles.append({
                "time": int(rate['time']),      # Unix timestamp
                "open": rate['open'],
                "high": rate['high'],
                "low": rate['low'],
                "close": rate['close']
            })
        return candles

