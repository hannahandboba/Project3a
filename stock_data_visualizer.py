from flask import Flask, render_template, request
import requests
from datetime import datetime
import pygal

# used this as basis https://github.com/IkeHasAPlan/Stock-Data-Visualizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    key = "IZ2BMG7IZUT81I82"
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    time_series = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    data = retrieve_data(time_series, symbol, key)
    chart = make_graph(data, chart_type)
    
    chart_svg = chart.render()

    return render_template('index.html', chart_svg=chart_svg)

def make_graph(data, chart_type):
    if chart_type == "line":
        chart = pygal.Line()
    elif chart_type == "bar":
        chart = pygal.Bar()
    else:
        return None

    if data:
        dates = data['dates']
        opens = data['open']
        highs = data['high']
        lows = data['low']
        closes = data['close']

        chart.add('Dates', dates)
        chart.add('Open', opens)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Close', closes)

    return chart

def retrieve_data(function, symbol, api_key):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()

            if 'Time Series' in data:
                time_series = data['Time Series']

                dates = []
                opens = []
                highs = []
                lows = []
                closes = []

                for date, values in time_series.items():
                    dates.append(date)
                    opens.append(float(values['open']))
                    highs.append(float(values['high']))
                    lows.append(float(values['low']))
                    closes.append(float(values['close']))

                return {
                    'dates': dates,
                    'open': opens,
                    'high': highs,
                    'low': lows,
                    'close': closes
                }
            else:
                print("Error: Data not found.")
        else:
            print(f"Error: {response.status_code}.")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")

    return None

if __name__ == '__main__':
    app.run(debug=True)