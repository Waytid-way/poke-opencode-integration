import logging
import asyncio
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from app.mt5_client import MT5Client
from app.risk import RiskManager
from app.logger import setup_logger

# Initialize FastMCP server
mcp = FastMCP("MT5-Local-Server")
setup_logger()
logger = logging.getLogger("mt5_mcp")

# Global state for clients
mt5_client: Optional[MT5Client] = None
risk_manager: Optional[RiskManager] = None

@mcp.on_startup()
async def startup() -> None:
    global mt5_client, risk_manager
    logger.info("Starting up MT5 integration...")
    mt5_client = MT5Client()
    if not mt5_client.initialize():
        raise RuntimeError("MT5 initialization failed")
    risk_manager = RiskManager(mt5_client)

@mcp.on_shutdown()
async def shutdown() -> None:
    global mt5_client
    if mt5_client:
        logger.info("Shutting down MT5 integration...")
        await asyncio.to_thread(mt5_client.shutdown)

@mcp.tool()
async def get_account_info() -> Dict[str, Any]:
    """Get MetaTrader 5 account information."""
    if not mt5_client:
        return {"error": "MT5 client not initialized"}
    return await asyncio.to_thread(mt5_client.get_account_info)

@mcp.tool()
async def place_order(symbol: str, order_type: str, volume: float, price: Optional[float] = None) -> Dict[str, Any]:
    """Place a trade on MT5 with risk validation."""
    if not mt5_client or not risk_manager:
        return {"error": "Server not fully initialized"}
    
    # Run risk validation in thread as it calls MT5 functions
    is_valid = await asyncio.to_thread(risk_manager.validate_trade, symbol, volume, order_type)
    if not is_valid:
        return {"error": "Risk validation failed: insufficient margin or exposure limit exceeded"}
    
    return await asyncio.to_thread(mt5_client.place_order, symbol, order_type, volume, price)

if __name__ == "__main__":
    mcp.run()
