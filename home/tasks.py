from bucket import bucket


# TODO: can be async?
def all_bucket_object_task():
    result = bucket.get_object()
    return result
