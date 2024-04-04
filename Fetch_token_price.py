
# Fetching price of a token
# Import necessary libraries
import requests
import json

# Function to fetch the current price of a token on Uniswap
def fetch_uniswap_price(token_address):
    # The Graph API URL for Uniswap
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

    # GraphQL query to fetch the price of the token
    query = """
    {
      token(id: "%s") {
        name
        symbol
        tradeVolumeUSD
        totalLiquidity
      }
    }
    """ % token_address

    # Send the request to the Uniswap Subgraph
    response = requests.post(url, json={'query': query})
    data = response.json()

    # Extract token information
    token_data = data['data']['token']
    if token_data:
        print(f"Token Name: {token_data['name']}")
        print(f"Symbol: {token_data['symbol']}")
        print(f"Trade Volume (USD): {token_data['tradeVolumeUSD']}")
        print(f"Total Liquidity: {token_data['totalLiquidity']}")
    else:
        print("Token data not found.")

# Example Token Address (DAI on Ethereum)
token_address = "0x6b175474e89094c44da98b954eedeac495271d0f"

# Fetch and print the price of DAI
fetch_uniswap_price(token_address)
