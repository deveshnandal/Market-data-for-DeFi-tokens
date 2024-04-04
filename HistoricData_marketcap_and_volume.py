############################################################################
### Historical data comparison for market cap and volume over time #########
### additional tokens that broadens the analysis ###########################

# Import necessary libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch historical data for a given token from CoinGecko
def fetch_coingecko_historical_data(token_id, days='max', interval='daily'):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': interval
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data['prices'], columns=['timestamp', 'Price (USD)']), \
               pd.DataFrame(data['market_caps'], columns=['timestamp', 'Market Cap (USD)']), \
               pd.DataFrame(data['total_volumes'], columns=['timestamp', 'Total Volume (USD)'])
    except requests.RequestException as e:
        print(f"Error fetching historical data for {token_id}: {e}")
        return None, None, None

# Tokens to include in our analysis
token_ids = [
    "dai",
    "compound-governance-token",
    "usd-coin",
    # Add additional tokens here
]

# Dates for the analysis
days = 90  # last 90 days
interval = 'daily'

# Initialize an empty list to store the data
historical_data = []

# Fetch historical data for each token
for token_id in token_ids:
    prices_df, market_caps_df, volumes_df = fetch_coingecko_historical_data(token_id, days, interval)
    if prices_df is not None and market_caps_df is not None and volumes_df is not None:
        prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
        market_caps_df['timestamp'] = pd.to_datetime(market_caps_df['timestamp'], unit='ms')
        volumes_df['timestamp'] = pd.to_datetime(volumes_df['timestamp'], unit='ms')

        historical_data.append({
            'token_id': token_id,
            'prices': prices_df,
            'market_caps': market_caps_df,
            'volumes': volumes_df
        })

# Plot the historical market caps and volumes
plt.figure(figsize=(14, 7))

# Plot market cap and volume for each token
for data in historical_data:
    plt.plot(data['market_caps']['timestamp'], data['market_caps']['Market Cap (USD)'],
             label=f"{data['token_id']} Market Cap")
    plt.plot(data['volumes']['timestamp'], data['volumes']['Total Volume (USD)'],
             label=f"{data['token_id']} Volume", linestyle='--')

plt.xlabel('Date')
plt.ylabel('USD')
plt.title('Historical Market Cap and Volume Comparison')
plt.legend()
plt.show()
