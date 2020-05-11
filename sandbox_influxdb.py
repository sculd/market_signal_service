import datetime, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

_TOKEN = 'TG1LH76GVHihj6as2H18rFiLx-q8Vd7E6m8KiHs9mZcrNJ_WTrS0xO6Y6Z-JNacWsqEMkvJknG8VeHs6x3-X5Q=='


# You can generate a Token from the "Tokens Tab" in the UI
_ORG = "market_signal"
bucket = "market_signal"

client = InfluxDBClient(url="https://us-central1-1.gcp.cloud2.influxdata.com", token=_TOKEN, org=_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

#'''
p = Point("timeseries_dummy").\
    tag("exchange", "kraken").\
    tag("symbol", "btcusd").\
    field("close", 7000.10)
write_api.write(bucket=bucket, record=p)

#'''



query_api = client.query_api()


records = query_api.query_stream('from(bucket:"{bucket}") |> range(start: -30m)'.format(
    bucket=bucket
))

for record in records:
    print(record)


