# Here go your api methods.

import url_signer
from gluon.utils import web2py_uuid

BUCKET_NAME = '/luca-teaching-images/'

@auth.requires_signature()
def notify_upload():
    post_id = int(request.vars.post_id)
    # TODO: Delete existing image name from GCS if any.
    db.uploaded_images.update_or_insert(
        (db.uploaded_images.post_id == post_id),
        image_name = request.vars.image_name,
        post_id = post_id,
    )
    return "ok"

@auth.requires_signature(hash_vars=False)
def get_image():
    post_id = int(request.vars.post_id)
    r = db(db.uploaded_images.post_id == post_id).select().first()
    if r is None:
        image_url = None
    else:
        # Produce a signed URL for GET.
        # Invents a random name for the image.
        image_url = url_signer.gcs_url(r.image_name, verb='GET', expiration_secs=3600)
    return response.json(dict(image_url=image_url))

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
