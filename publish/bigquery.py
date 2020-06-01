import os, datetime
import util.bigquery

_PUBLISH_QUERY_FORMAT = (
    """
    INSERT `sudden_price_changes.sudden_price_changes` (timestamp, exchange, symbol, change_window_minutes, change_threshold, change, price)
    VALUES{values}    
    """
    )


def _get_values_strs(exchange, column_dicts):
    def epoch_seconds_to_utc_datetime_str(epoch_seconds):
        return datetime.datetime.utcfromtimestamp(epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')

    def _get_values_str(column_dict):
        return "('{timestamp}', '{exchange}', '{symbol}', {change_window_minutes}, {change_threshold}, {change}, {price})".format(
            timestamp = epoch_seconds_to_utc_datetime_str(column_dict['time']),
            exchange = exchange,
            symbol=column_dict['symbol'],
            change_window_minutes=column_dict['change_window_minutes'],
            change_threshold=column_dict['change_threshold'],
            change=column_dict['change'],
            price=column_dict['price']
        )

    res = ',\n'.join([_get_values_str(c_d) for c_d in column_dicts])
    print('inserting {n} items with the following values: {values}'.format(
        n=len(column_dicts),
        values =res
        )
        )
    return res


def publish(exchange, column_dicts):
    util.bigquery.get_client().query(
        _PUBLISH_QUERY_FORMAT.format(
            values = _get_values_strs(exchange, column_dicts)
            )
        )
