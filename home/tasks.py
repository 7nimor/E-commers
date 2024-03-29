from bucket import bucket
from celery import shared_task


# TODO: can be async?
def all_bucket_object_task():
    result = bucket.get_objects()
    return result


@shared_task
def delete_bucket_object_task(key):
    bucket.delete_object(key=key)


@shared_task
def download_bucket_object_task(key):
    bucket.download_object(key)


@shared_task
def upload_bucket_object_task(req=None, field=None):
    bucket.upload_object(req, field)
