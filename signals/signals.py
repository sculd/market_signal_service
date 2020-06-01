import util.bigquery

_QUERY = '''
    SELECT timestamp, exchange, symbol, change_window_minutes, change_threshold, AVG(change) AS change, AVG(price) AS price
    FROM `alpaca-trading-239601.sudden_price_changes.sudden_price_changes` 
    #WHERE change_threshold > 0.05
    GROUP BY timestamp, exchange, symbol, change_window_minutes, change_threshold
    ORDER BY timestamp DESC
    LIMIT 100
'''

def get_signals():
    query_job = util.bigquery.get_client().query(_QUERY)

    rows = query_job.result()

    res = []
    for row in rows:
        res.append({
            'timestamp': row.timestamp,
            'exchange': row.exchange,
            'symbol': row.symbol,
            'change_window_minutes': row.change_window_minutes,
            'change_threshold': row.change_threshold,
            'change': row.change,
            'price': row.price
        })

    return res
