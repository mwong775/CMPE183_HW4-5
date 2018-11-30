import base64
import json
import os
import time
import urllib

import url_signer

@auth.requires_signature()
def get_upload_url():
    """Returns a fresh URL with ID to post something to GCS.
    It returns a dictionary with two fields:
    - upload_url: used for uploading
    - download_url: used for retrieving the content"""
    # Invents a random name for the image.
    image_path = BUCKET_NAME + web2py_uuid() + ".jpg"
    signed_put_url = url_signer.gcs_url(image_path, verb='PUT', content_type='image/jpeg')
    # signed_get_url = gcs_url(image_path, verb='GET',
    #                          expiration_secs=3600 * 24 * 365)
    # This line is required; otherwise, cross-domain requests are not accepted.
    # response.headers['Access-Control-Allow-Origin'] = '*'
    return response.json(dict(
        signed_url=signed_put_url,
        image_name=image_path
    ))
