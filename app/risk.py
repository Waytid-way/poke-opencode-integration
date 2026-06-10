import logging
from typing import Any, Optional
import MetaTrader5 as mt5

logger = logging.getLogger("mt5_mcp")

class RiskManager:
    def __init__(self, mt5_client: Any, max_exposure_ratio: float = 0.1):
        self.mt5_client = mt5_client
        self.max_exposure_ratio = max_exposure_ratio

    def validate_trade(self, symbol: str, volume: float, order_type: str) -> bool:
        """
        Validate margin and limits against mt5.account_info().
        """
        logger.info(f"Validating trade: {symbol} {volume} {order_type}")
        
        account_info = mt5.account_info()
        if account_info is None:
            logger.error("Failed to get account info for risk validation")
            return False

        # Basic check for symbol existence and volume limits
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Symbol {symbol} info not found")
            return False

        # Check volume limits
        if volume < symbol_info.volume_min or volume > symbol_info.volume_max:
            logger.error(f"Volume {volume} out of bounds [{symbol_info.volume_min}, {symbol_info.volume_max}]")
            return False

        # 1. Calculate Margin Requirement
        if order_type.lower() == 'buy':
            mt5_order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        elif order_type.lower() == 'sell':
            mt5_order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        else:
            logger.error(f"Invalid order type: {order_type}")
            return False

        margin_required = mt5.order_calc_margin(mt5_order_type, symbol, volume, price)
        if margin_required is None:
            logger.error(f"Failed to calculate margin for {symbol}")
            return False
        
        if margin_required > account_info.margin_free:
            logger.warning(f"Insufficient margin: Required {margin_required}, Available {account_info.margin_free}")
            return False

        # 2. Exposure Check
        positions = mt5.positions_get(symbol=symbol)
        current_volume = sum(p.volume for p in positions) if positions else 0.0
        
        max_exposure = account_info.equity * self.max_exposure_ratio
        new_exposure = (current_volume + volume) * symbol_info.trade_contract_size * price
        
        if new_exposure > max_exposure:
            logger.warning(f"Exposure limit exceeded: New Exposure {new_exposure}, Max Exposure {max_exposure}")
            return False

        return True
