import random
import string
ARVAN_USER_IMAGE_URL = 'https://user-image-gallery.s3.ir-thr-at1.arvanstorage.com/'

import boto3
from django.conf import settings


class Bucket:
    """CDN bucket manager
    init method for bucket connection

    NOTE:
        none of these methods are async. uer public instance is tasks.py modules instead.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self,req=None, field=None):
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        if req.data[field] != "":
            self.conn.upload_object(
                image_data=req.data[field],
                bucket_name="user-image-gallery",
                object_name="{0}.jpg".format(str(ran))
            )
            req.data.pop(field)
            req.data[field] = ARVAN_USER_IMAGE_URL + "{0}.jpg".format(str(ran))
        elif req.data[field] == "":
            req.data[field] = "empty"
        return req


bucket = Bucket()
