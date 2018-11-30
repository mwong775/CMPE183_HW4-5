# Here go your api methods.

import url_signer

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

