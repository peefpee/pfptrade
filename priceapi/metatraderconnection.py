import MetaTrader5 as mt5

class metatrader:
    def __init__(self):
        self.initialized = False
        self.symbols = self.getallsymbols()

    def initialize(self):
        if not mt5.initialize():
            raise Exception(f"Failed to initialize MetaTrader5 API, error : {mt5.last_error()}")
        else:
            self.initialized = True
    def getallsymbols(self):
        if not self.initialized:
            raise Exception("Not connected to MetaTrader 5")
        
        symbols = mt5.symbols_get()
        return [symbol.name for symbol in symbols]
    def symbol_info_tick(self, symbol):

        if not self.initialized:
            raise Exception("Not connected to MetaTrader 5")
        if symbol not in self.symbols:
            raise Exception(f"Symbol {symbol} not found in MetaTrader 5 symbols list")
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise Exception(f"Failed to get tick info for symbol {symbol}, error: {mt5.last_error()}")
        
        return tick
