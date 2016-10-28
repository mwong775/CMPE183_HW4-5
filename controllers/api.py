import io

def index():
    pass

# Mocks implementation.
def get_tracks():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    tracks = []
    has_more = False
    rows = db().select(db.track.ALL, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            # Check if I have a track or not.
            track_url = URL('api', 'play_track', vars=dict(track_id=r.id)) if r.has_track else None
            t = dict(
                id = r.id,
                artist = r.artist,
                album = r.album,
                title = r.title,
                duration = r.duration,
                rating = r.rating,
                num_plays = r.num_plays,
                track_url = track_url,
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
    data_stream = io.BytesIO(t.data_blob)
    return response.stream(data_stream, chunk_size=4096)
