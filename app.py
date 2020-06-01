import json, os, time, logging, threading
logging.basicConfig(level=logging.DEBUG)

from enum import Enum
from flask import Flask, request, render_template
from flask_caching import Cache
import flask_cors
from flask_cors import CORS
from collections import defaultdict
import config
import util.logging
import signals.signals

_EXCHANGES_FILENAME = 'exchanges.json'
_MARKETS_FILENAME = 'markets.json'
_EXCHANGE_MARKETS_FILENAME = 'exchange_markets.json'

_exchanges = json.load(open(_EXCHANGES_FILENAME))
_markets = json.load(open(_MARKETS_FILENAME))
_exchange_markets = json.load(open(_EXCHANGE_MARKETS_FILENAME))

RESPONSE_KEY_EXCHANGES = 'exchanges'
RESPONSE_KEY_SYMBOLS = 'symbols'

class FAULT_CODE_GENERATING_TRAFFIC_MODE(Enum):
    OK = 1
    INVALID_API_KEY = 2
    INVALID_ACCESS_TOKEN = 2
    GENERATE_ACCESS_TOKEN = 3
    BAD_REQUEST = 4


cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}
app = Flask(__name__)
CORS(app, allow_headers='*', origins='*', methods='*', expose_headers='Authorization')
app.config.from_mapping(cache_config)
cache = Cache(app)

def _get_available_exchanges():
    return config.get_available_exchanges()

def _get_exposed_exchanges():
    available_exchanges = set(config.get_available_exchanges())
    return [e for e in _exchanges.values() if e in available_exchanges]

@app.route('/exchanges', methods=['GET'])
@cache.cached(timeout=60)
def get_exchanges():
    return {RESPONSE_KEY_EXCHANGES: _get_exposed_exchanges()}

@app.route('/symbols', methods=['GET'])
@cache.cached(timeout=60)
def get_symbols():
    a_exchange = request.args.get('exchange')
    res = defaultdict(list)
    exposed_exchanges = set(_get_exposed_exchanges())
    for exchange, symbols in _exchange_markets.items():
        if a_exchange and a_exchange != exchange: continue
        if exchange not in exposed_exchanges: continue
        for symbol in symbols:
            res[exchange].append(symbol) 
    return res

@app.route('/signals', methods=['GET'])
def get_signals():
    ss = {'signals': signals.signals.get_signals()}
    return ss

@app.route("/chart")
@flask_cors.cross_origin(origin='*')
def home():
    symbol = request.args.get('symbol')
    if not symbol:
        return 'invalid request'
    return render_template("chart.html", symbol=symbol.upper())


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    config.load()
    app.run(host='localhost', port=8081, debug=True)
