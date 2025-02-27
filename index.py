from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/get_data', methods=['GET'])
def get_data():
    # Example GET endpoint implementation
    ticker = 'IOC.NS'
    df = yf.download(ticker=ticker)
    if df.empty:
        return jsonify({"error": "No data found for the ticker"})
    
    # Convert to JSON and return
    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/post_data', methods=['POST'])
def post_data():
    # Get the JSON data from the request body
    data = request.get_json()

    sym = (data['symbol'].strip().upper()) + '.NS'
    print(sym)

    df = yf.download(tickers=sym, start=data['start'], end=data['end'], interval=data['interval'])
    df.columns=['close','high','low','open','volume']
    datetime_series = df.index

    # Convert the datetime series to a datetime format
    datetime_series = pd.to_datetime(datetime_series)

    # Format the datetime values to 'yyyy-mm-dd' format
    df.index = datetime_series.strftime('%Y-%m-%d')

    # Process the data (in this example, we'll just echo it back)
    if len(df):
        df['time'] = df.index.astype(str)
        # df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"}, inplace=True)
        if df.time[0] == df.time[1]:
            df.time = range(len(df))

        a = df.to_dict(orient='records')

        rtn = a

    return jsonify(rtn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000)
