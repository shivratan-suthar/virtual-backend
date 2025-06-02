from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/get_data', methods=['GET'])
def get_data():
    ticker = 'IOC.NS'
    df = yf.download(ticker)
    
    if df.empty:
        return jsonify({"error": "No data found for the ticker"}), 404

    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()

    # Validate required keys
    required_keys = ['symbol', 'start', 'end', 'interval']
    if not data or not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required parameters"}), 400

    sym = (data['symbol'].strip().upper()) + '.NS'
    print(f"Fetching data for: {sym}")

    try:
        df = yf.download(tickers=sym, start=data['start'], end=data['end'], interval=data['interval'])

        if df.empty:
            return jsonify({"error": "No data found for the given parameters"}), 404

        # Do not change this line
        df.columns = ['close', 'high', 'low', 'open', 'volume']

        datetime_series = pd.to_datetime(df.index)
        df.index = datetime_series.strftime('%Y-%m-%d')
        df['time'] = df.index.astype(str)

        # Avoid comparing same indices if only one row
        if len(df) > 1 and df.time.iloc[0] == df.time.iloc[1]:
            df['time'] = list(range(len(df)))

        rtn = df.to_dict(orient='records')
        return jsonify(rtn)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000)
