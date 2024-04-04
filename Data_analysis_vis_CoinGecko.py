###### Data analyis and Visualization using CoinGecko API ########
##################################################################

# Import necessary libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch token data from CoinGecko
def fetch_coingecko_token_data(token_id):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        market_data = data['market_data']
        if market_data:
            return {
                'Name': data['name'],
                'Symbol': data['symbol'],
                'Price (USD)': market_data['current_price']['usd'],
                'Market Cap (USD)': market_data['market_cap']['usd'],
                'Total Volume (USD)': market_data['total_volume']['usd']
            }
    except requests.RequestException as e:
        print(f"Error fetching data for {token_id}: {e}")
    return None

# List of CoinGecko token IDs to fetch data for
token_ids = [
    "dai",      # DAI
    "compound-governance-token", # COMP
    "usd-coin"  # USDC
]

# Fetch data for each token and filter out failures
token_data_list = [fetch_coingecko_token_data(token_id) for token_id in token_ids]
token_data_list = [data for data in token_data_list if data is not None]

# Convert list of token data to a DataFrame
df_tokens = pd.DataFrame(token_data_list)

# Data Normalization using Logarithmic Scale
df_tokens['Log Market Cap (USD)'] = np.log(df_tokens['Market Cap (USD)'])
df_tokens['Log Total Volume (USD)'] = np.log(df_tokens['Total Volume (USD)'])

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Token')
ax1.set_ylabel('Log Market Cap (USD)', color=color)
ax1.bar(df_tokens['Symbol'], df_tokens['Log Market Cap (USD)'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Log Total Volume (USD)', color=color)
ax2.plot(df_tokens['Symbol'], df_tokens['Log Total Volume (USD)'], color=color, marker='o', linestyle='none')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title('Comparative Analysis of DeFi Tokens Using CoinGecko Data')
plt.show()
