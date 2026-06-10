import logging

logger = logging.getLogger("mt5_mcp")

class RiskManager:
    def __init__(self, max_exposure=1.0):
        self.max_exposure = max_exposure

    def validate_trade(self, symbol, volume):
        """Basic risk check logic."""
        logger.info(f"Validating trade: {symbol} {volume}")
        # Add actual risk logic here (e.g., check account balance, open positions)
        return True
