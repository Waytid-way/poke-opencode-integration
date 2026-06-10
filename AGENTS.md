# Poke & Opencode MT5 MCP Integration

This project implements a local Windows-based MetaTrader 5 (MT5) MCP server using the FastMCP framework. It allows AI agents (like Poke and Opencode) to interact with MT5 safely.

## Architecture

1.  **Poke (Orchestrator):** Acts as the high-level interface, handling user requests and delegating complex coding/execution tasks.
2.  **Opencode:** Can be used to refine the MCP server logic or generate trading strategies that leverage this MCP server.
3.  **FastMCP Server:** A Python-based server running locally on Windows that communicates with the MT5 terminal via the `MetaTrader5` library.

## Safety Controls

-   **Risk Manager (`app/risk.py`):** Every trade request is intercepted by the Risk Manager to ensure it stays within predefined exposure limits.
-   **Local Execution:** The server runs on your local machine, giving you full control over when the trading interface is active.
-   **Structured Logging:** All actions are logged to the console for real-time monitoring of agent activity.

## Setup

1.  Install MT5 on Windows.
2.  Install dependencies: `pip install mcp MetaTrader5`.
3.  Run the server: `python app/main.py`.
