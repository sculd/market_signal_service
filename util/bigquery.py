import os
from google.cloud import bigquery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')

_client = None

def get_client():
    global _client
    if not _client:
        _client = bigquery.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    return _client

