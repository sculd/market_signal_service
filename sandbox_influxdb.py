import datetime, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_TOKEN = ''


# You can generate a Token from the "Tokens Tab" in the UI
_ORG = "market_signal"
bucket = "sandbox"

client = InfluxDBClient(url="https://us-central1-1.gcp.cloud2.influxdata.com", token=_TOKEN, org=_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

'''
p = Point("simple_sudden_move").\
    tag("symbol", "btcusd").\
    tag("change_window_minutes", 60).\
    tag("change_threshold", 0.05).\
    field("price", 8000.10).\
    field("change", 0.7)
write_api.write(bucket=bucket, record=p)

#'''



query_api = client.query_api()


records = query_api.query_stream('from(bucket:"{bucket}") |> range(start: -30m)'.format(
    bucket=bucket
))

for record in records:
    print(record)


