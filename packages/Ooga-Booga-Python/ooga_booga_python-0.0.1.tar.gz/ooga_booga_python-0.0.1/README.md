# Ooga Booga Python Client

The **Ooga Booga Python Client** is a wrapper for the [Ooga Booga API V1](https://docs.oogabooga.io/api/), a powerful DEX aggregation and smart order routing REST API built to integrate Berachain's liquidity into your DApp or protocol. This client allows you to interact with Berachain's liquidity sources, including AMMs, bonding curves, and order books, to execute the best trades with minimal price impact.

For more details on the API and its capabilities, refer to the official [Ooga Booga API Documentation](https://docs.oogabooga.io/api/).

## Features

- 💸 **Find the Best Rates**: Get optimal real-time prices for your trades by leveraging Ooga Booga's liquidity aggregation.
- 🚀 **Simplified Integration**: A single API integration grants access to all liquidity sources on Berachain, saving you development time.
- 📈 **Optimal Trade Execution**: Perform efficient trades with minimized price impact and maximum returns for your users.
- 🦺 **Enhanced Security**: Execute trades securely via Ooga Booga’s smart contract, which wraps each transaction.
- Asynchronous API calls using `aiohttp` for smooth, non-blocking operations.

## Features

- Fetch token lists and prices
- Approve token allowances
- Query token allowances
- Perform token swaps
- Retrieve liquidity sources
- Comprehensive error handling
- Asynchronous API calls using `aiohttp`

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

To install the package, clone this repository and use the `setup.py` file:

```bash
git clone <repository-url>
cd ooga_booga_python
pip install .
```

Or add it to your project by adding it to your `requirements.txt` file.

---

## Setup

1. Copy the `example_env.env` file to `.env`:

```bash
cp tests/example_env.env .env
```

2. Add your API key and private key:

```plaintext
OOGA_BOOGA_API_KEY="your-api-key"
PRIVATE_KEY="your-private-key"
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Here’s how to use the **Ooga Booga Python Client** in your project:

### Initialize the Client

```python
from ooga_booga_python.client import OogaBoogaClient
import asyncio

async def main():
    client = OogaBoogaClient(
        api_key="your-api-key",
        private_key="your-private-key"
    )
    # Example: Fetch token list
    tokens = await client.get_token_list()
    for token in tokens:
        print(f"Name: {token.name}, Symbol: {token.symbol}")

asyncio.run(main())
```

### Perform a Token Swap

```python
from ooga_booga_python.models import SwapParams

async def perform_swap(client):
    swap_params = SwapParams(
        tokenIn="0xTokenInAddress",
        amount=1000000000000000000,  # 1 token in wei
        tokenOut="0xTokenOutAddress",
        to="0xYourWalletAddress",
        slippage=0.02,
    )
    await client.swap(swap_params)

asyncio.run(perform_swap(client))
```

### Get Token Prices

```python
async def fetch_prices(client):
    prices = await client.get_token_prices()
    for price in prices:
        print(f"Token: {price.address}, Price: {price.price}")

asyncio.run(fetch_prices(client))
```

---

## API Reference

### `OogaBoogaClient`

#### Initialization

```python
client = OogaBoogaClient(api_key: str, private_key: str, rpc_url: str = "https://bartio.rpc.berachain.com/")
```

- **`api_key`**: Your API key for authentication.
- **`private_key`**: Your private key for signing transactions.
- **`rpc_url`**: (Optional) RPC URL for blockchain interaction.

#### Methods

1. **`get_token_list()`**  
   Fetches the list of available tokens.

2. **`get_token_prices()`**  
   Fetches the current prices of tokens.

3. **`get_liquidity_sources()`**  
   Fetches all available liquidity sources.

4. **`swap(swap_params: SwapParams)`**  
   Performs a token swap using the provided parameters.

5. **`approve_allowance(token: str, amount: str = MAX_INT)`**  
   Approves a token allowance for the router.

6. **`get_token_allowance(from_address: str, token: str)`**  
   Fetches the allowance of a token for a specific address.

---

## Testing

The package uses `pytest` for testing. To run the tests:

1. Install test dependencies:

```bash
pip install -r requirements.txt
```

2. Run the tests:

```bash
pytest tests/
```

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).