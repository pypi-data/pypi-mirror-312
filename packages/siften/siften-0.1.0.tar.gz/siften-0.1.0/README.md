# Siften

A Python library for Siften.

## Installation

```bash
pip install siften
```

## Quick Start

```python
from siften import execute_strategy

# Execute a trading strategy
strategy_result = execute_strategy(
    user_id="user123",
    agent_id="agent456",
    symbol="BTCUSDT",
    quantity=0.001,
    exchange="Binance",
    strategy="Trend Following",
    stop_loss=0.02,  # 2% stop loss
    profit_take=0.05  # 5% take profit
)
```

## Trading Strategy Execution

The `execute_strategy` function allows you to implement trading strategies with customizable parameters:

| Parameter   | Type  | Description                          |
| ----------- | ----- | ------------------------------------ |
| user_id     | str   | User identifier                      |
| agent_id    | str   | Agent identifier                     |
| symbol      | str   | Trading pair symbol                  |
| quantity    | float | Trading quantity                     |
| exchange    | str   | Exchange name                        |
| strategy    | str   | Strategy name                        |
| stop_loss   | float | Stop loss percentage                 |
| profit_take | float | Take profit percentage               |
| time_left   | int   | Remaining execution time (optional)  |
| request_id  | str   | Unique request identifier (optional) |

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```
