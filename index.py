from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd 
import yfinance as yf
import os

app = Flask(__name__)
CORS(app)

@app.route('/post_data', methods=['POST'])
def post_data():
    # Get the JSON data from the request body
    data = request.get_json()

    try:
        sym = (data['symbol'].strip().upper()) + '.NS'
        print(sym)

        df = yf.download(tickers=sym, start=data['start'], end=data['end'], interval=data['interval'])
        datetime_series = df.index

        # Convert the datetime series to a datetime format
        datetime_series = pd.to_datetime(datetime_series)

        # Format the datetime values to 'yyyy-mm-dd' format
        df.index = datetime_series.strftime('%Y-%m-%d')

        # Process the data
        if len(df):
            df['time'] = df.index.astype(str)
            df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"}, inplace=True)
            if df.time[0] == df.time[1]:
                df.time = range(len(df))
            
            data_records = df.to_dict(orient='records')
            response_data = data_records
        else:
            response_data = []

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 2000))
    app.run(host="0.0.0.0", port=port)
