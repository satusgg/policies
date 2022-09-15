import functions_framework
from google.cloud import storage
import time

# CloudEvent function to be triggered by an Eventarc Cloud Audit Logging trigger
# Note: this is NOT designed for second-party (Cloud Audit Logs -> Pub/Sub) triggers!
@functions_framework.cloud_event
def hello_auditlog(cloudevent):
    #default retention period (20 days in this case)
    retention_period= 1728000
    payload = cloudevent.data.get("protoPayload")
    if(payload):
        # Checking the name of the bucket that has been created
        bucket_name=payload.get('resourceName').split('/')[-1]
        # Obtaining the GCS
        storage_client=storage.Client()
        # Obtaining the bucket that has been created
        bucket = storage_client.get_bucket(bucket_name)
        # Checking if the retention period is not yet set
        if bucket.retention_period is None:
            # Setting the rettention period to the default one
            bucket.retention_period=retention_period
            #Setting the bucket lock.
            bucket.lock_retention_policy()
            # Patching the bucket
            bucket.patch()
            # Waits the lock to propagate
            time.sleep(10)
            bucket.lock_retention_policy()
            bucket.patch()