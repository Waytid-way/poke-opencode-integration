import MetaTrader5 as mt5
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("mt5_mcp")

class MT5Client:
    def __init__(self) -> None:
        pass

    def initialize(self) -> bool:
        if not mt5.initialize():
            logger.error(f"MT5 initialization failed, error code: {mt5.last_error()}")
            return False
        logger.info("MT5 initialized successfully")
        return True

    def get_account_info(self) -> Dict[str, Any]:
        account_info = mt5.account_info()
        if account_info is None:
            return {"error": f"Failed to get account info, error code: {mt5.last_error()}"}
        return account_info._asdict()

    def place_order(self, symbol: str, order_type: str, volume: float, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Implementation for MT5 order placement using trade types for buy/sell.
        order_type should be 'buy' or 'sell'.
        """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return {"error": f"Symbol {symbol} not found"}
        
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                return {"error": f"Failed to select symbol {symbol}"}

        if order_type.lower() == 'buy':
            trade_type = mt5.ORDER_TYPE_BUY
            if price is None:
                tick = mt5.symbol_info_tick(symbol)
                if tick is None:
                    return {"error": "Could not get tick info"}
                price = tick.ask
        elif order_type.lower() == 'sell':
            trade_type = mt5.ORDER_TYPE_SELL
            if price is None:
                tick = mt5.symbol_info_tick(symbol)
                if tick is None:
                    return {"error": "Could not get tick info"}
                price = tick.bid
        else:
            return {"error": f"Invalid order type: {order_type}. Must be 'buy' or 'sell'."}

        request: Dict[str, Any] = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": trade_type,
            "price": float(price),
            "magic": 123456,
            "comment": "Poke OpenCode Integration",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None:
            return {"error": f"Order send failed, error code: {mt5.last_error()}"}
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {"error": f"Order failed, retcode: {result.retcode}", "result": result._asdict()}
            
        return result._asdict()

    def shutdown(self) -> None:
        mt5.shutdown()
        logger.info("MT5 shutdown successfully")
