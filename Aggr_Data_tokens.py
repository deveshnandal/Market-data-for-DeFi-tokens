####################################################
## Aggregating data from multiple tokens ###########
####################################################
# Import pandas for data manipulation
import pandas as pd

# Modified function to return token data instead of printing it
def fetch_uniswap_token_data(token_address):
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
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
    response = requests.post(url, json={'query': query})
    data = response.json()

    # Return token data as a dictionary
    token_data = data['data']['token']
    if token_data:
        return {
            'Name': token_data['name'],
            'Symbol': token_data['symbol'],
            'Trade Volume (USD)': float(token_data['tradeVolumeUSD']),
            'Total Liquidity': float(token_data['totalLiquidity'])
        }
    else:
        return None

# List of token addresses to fetch data for
token_addresses = [
    "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI
    "0xc00e94Cb662C3520282E6f5717214004A7f26888", # COMP
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
]

# Fetch data for each token and store in a list
token_data_list = []
for address in token_addresses:
    token_data = fetch_uniswap_token_data(address)
    if token_data:
        token_data_list.append(token_data)

# Convert list of token data to a DataFrame
df_tokens = pd.DataFrame(token_data_list)

print(df_tokens)
