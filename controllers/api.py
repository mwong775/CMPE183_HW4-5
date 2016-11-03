import tempfile

def index():
    pass

def get_tracks():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # Gets the variables for the sorting.
    orderby = db.track.artist
    if request.vars.sort_artist is not None:
        orderby = db.track.artist if request.vars.sort_artist == 'up' else ~db.track.artist
    if request.vars.sort_track is not None:
        orderby = db.track.title if request.vars.sort_track == 'up' else ~db.track.title
    tracks = []
    has_more = False
    rows = db().select(db.track.ALL,
                       orderby=orderby,
                       limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            # Check if I have a track or not.
            t = dict(
                id = r.id,
                artist = r.artist,
                album = r.album,
                title = r.title,
                duration = r.duration,
                rating = r.rating,
                num_plays = r.num_plays,
                has_track = r.has_track,
            )
            tracks.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        tracks=tracks,
        logged_in=logged_in,
        has_more=has_more,
    ))

@auth.requires_signature()
def add_track():
    t_id = db.track.insert(
        artist = request.vars.artist,
        album = request.vars.album,
        title = request.vars.title,
        duration = request.vars.duration,
        rating = 0,
        num_plays = 0
    )
    t = db.track(t_id)
    return response.json(dict(track=t))

@auth.requires_signature()
def del_track():
    db(db.track.id == request.vars.track_id).delete()
    return "ok"

# TODO: used signed URLs.
def upload_track():
    track_id = int(request.vars.track_id)
    # If I already have music for that track, delete it.
    db(db.track_data.track_id == track_id).delete()
    # Reads the bytes of the track.
    logger.info("Uploaded a file of type %r" % request.vars.file.type)
    if not request.vars.file.type.startswith('audio'):
        raise HTTP(500)
    db.track_data.insert(
        track_id=track_id,
        original_filename=request.vars.file.filename,
        data_blob=request.vars.file.file.read(),
        mime_type=request.vars.file.type,
    )
    db(db.track.id == track_id).update(has_track=True)
    return "ok"

def play_track():
    track_id = int(request.vars.track_id)
    t = db(db.track_data.track_id == track_id).select().first()
    if t is None:
        return HTTP(404)
    headers = {}
    headers['Content-Type'] = t.mime_type
    # Web2py is setup to stream a file, not a data blob.
    # So we create a temporary file and we stream it.
    # f = tempfile.TemporaryFile()
    f = tempfile.NamedTemporaryFile()
    f.write(t.data_blob)
    f.seek(0) # Rewind.
    return response.stream(f.name, chunk_size=4096, request=request)
