###### Front end flask integration #######
##########################################
from flask import Flask, render_template, request
import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json

app = Flask(__name__)

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
        prices_df = pd.DataFrame(data['prices'], columns=['timestamp', 'Price (USD)'])
        market_caps_df = pd.DataFrame(data['market_caps'], columns=['timestamp', 'Market Cap (USD)'])
        volumes_df = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'Total Volume (USD)'])
        return prices_df, market_caps_df, volumes_df
    except requests.RequestException as e:
        print(f"Error fetching historical data for {token_id}: {e}")
        return None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_id = request.form.get('token_id')
        days = request.form.get('days')
        prices_df, market_caps_df, volumes_df = fetch_coingecko_historical_data(token_id, days)
        if prices_df is not None and market_caps_df is not None and volumes_df is not None:
            prices_df['Date'] = pd.to_datetime(prices_df['timestamp'], unit='ms').dt.date
            market_caps_df['Date'] = pd.to_datetime(market_caps_df['timestamp'], unit='ms').dt.date
            volumes_df['Date'] = pd.to_datetime(volumes_df['timestamp'], unit='ms').dt.date

            market_cap_trace = go.Scatter(x=market_caps_df['Date'], y=market_caps_df['Market Cap (USD)'],
                                          mode='lines', name='Market Cap')
            volume_trace = go.Scatter(x=volumes_df['Date'], y=volumes_df['Total Volume (USD)'],
                                      mode='lines', name='Volume')
            fig = go.Figure(data=[market_cap_trace, volume_trace])
            graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
            return render_template('index.html', graphJSON=graphJSON)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
