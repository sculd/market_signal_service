import datetime, os, json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')
from google.cloud import pubsub_v1
import util.logging

def run_loop(subscription_id):
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, subscription_id
    )

    def callback(message_payload):
        msg = json.loads(message_payload.data.decode('utf-8'))
        message_payload.ack()
        print(msg)
        util.logging.log_signal(msg)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback
    )
    print("Listening for messages on {}\n".format(subscription_path))

    try:
        streaming_pull_future.result()
    except Exception as ex:  # noqa
        streaming_pull_future.cancel()


if __name__ == '__main__':
    subscription_id = os.getenv('CRYPTOWATCH_PUBSUB_SIGNAL_SUBSCRIPTION_ID')
    run_loop(subscription_id)
