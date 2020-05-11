import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')

client = bigquery.Client()
query_job = client.query("""
    SELECT
      CONCAT(
        'https://stackoverflow.com/questions/',
        CAST(id as STRING)) as url,
      view_count
    FROM `alpaca-trading-239601.market_signal.market_signal`
    LIMIT 10""")

results = query_job.result()  # Waits for job to complete.




for row in results:
    print("{} : {} views".format(row.url, row.view_count))