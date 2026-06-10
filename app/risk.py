import logging
import MetaTrader5 as mt5

logger = logging.getLogger("mt5_mcp")

class RiskManager:
    def __init__(self, mt5_client, max_exposure_ratio=0.1):
        self.mt5_client = mt5_client
        self.max_exposure_ratio = max_exposure_ratio

    def validate_trade(self, symbol, volume):
        \"\"\"
        Validate margin and limits against mt5.account_info().
        \"\"\"
        logger.info(f"Validating trade: {symbol} {volume}")
        
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

        # Free margin check (example: ensure we aren't completely drained)
        if account_info.margin_free <= 0:
             logger.warning("No free margin available")
             return False
        
        return True
