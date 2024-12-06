# IQOption API Library

An updated Python library for interacting with the IQ Option platform using modern asynchronous features like `aiohttp` and `websockets`.

## Features
- Fully asynchronous.
- Supports real-time data streams (candles, balances, positions).
- Includes utilities for trading operations.

## Installation
Install the library (when published) via pip:
```bash
pip install iqoption_async
```

For development:
```bash
git clone https://github.com/yourusername/iqoption_async.git
cd iqoption_async
pip install -r requirements.txt
```

## Usage
### Initialization
The main client to interact with the API is IQOptionClient. Initialize it with your email and password:
```python
import asyncio
from iqoption_async.client import IQOptionClient

client = IQOptionClient(email="your_email@example.com", password="your_password")

async def main():
    success, reason = await client.connect()
    if success:
        print("Connected successfully!")
    else:
        print(f"Failed to connect: {reason}")

asyncio.run(main())
```

### Retrieving Profile Data
Fetch the user's profile:
```python
profile = await client.get_profile()
print(f"User ID: {profile.id}")
print(f"Balances: {profile.balances}")
```

### Changing Balance
Switch between practice and real accounts (PRACTICE, REAL):
```python
await client.change_balance("PRACTICE")
balance = await client.get_balance()
print(f"Current practice balance: {balance}")
```

### Fetching Candles
Retrieve candle data for a specific symbol:
```python
candles = await client.get_candles("EURUSD", interval_min=1, limit=10, end_time=time.time())
print(candles)
```

### Buying an Option
Place a trade:
```python
result, order_id, expiration = await client.buy(amount=10, symbol="EURUSD", action="call", expiration=1)
if result:
    print(f"Trade successful! Order ID: {order_id}")
else:
    print("Trade failed.")
    return

mins = math.ceil(((datetime.fromtimestamp(expiration) -  datetime.now()).seconds / 60))

# WAIT for result
finded, status, profit = await client.check_order(order_id, mins)
# status -> win, loose, equal, sold
if finded:
    print(f"Order with status {status} profit {profit}")
else:
    print("Order not found")

# ASYNC for result
async def func(result):
    finded, status, profit = result
await client.check_order(order_id, mins, func)
```