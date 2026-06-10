import logging
from mcp.server.fastmcp import FastMCP
from app.mt5_client import MT5Client
from app.risk import RiskManager
from app.logger import setup_logger

# Initialize FastMCP server
mcp = FastMCP("MT5-Local-Server")
setup_logger()
logger = logging.getLogger("mt5_mcp")

mt5_client = MT5Client()
risk_manager = RiskManager()

@mcp.tool()
async def get_account_info():
    """Get MetaTrader 5 account information."""
    return mt5_client.get_account_info()

@mcp.tool()
async def place_order(symbol: str, order_type: str, volume: float, price: float = None):
    """Place a trade on MT5 with risk validation."""
    if not risk_manager.validate_trade(symbol, volume):
        return {"error": "Risk validation failed"}
    return mt5_client.place_order(symbol, order_type, volume, price)

if __name__ == "__main__":
    mcp.run()
