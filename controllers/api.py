import random
import requests


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
            t = dict(
                id=r.id,
                artist=r.artist,
                album=r.album,
                title=r.title,
                duration=r.duration,
                rating=r.rating,
                num_plays=r.num_plays,
                track_source = r.track_source
            )

            if r.track_source == 'spotify':
                t['audio_file'] = "https://embed.spotify.com/?uri={}&theme=white".format(r.track_uri)
            else:
                t['audio_file'] = "#"
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
        artist=request.vars.artist,
        album=request.vars.album,
        title=request.vars.title,
        duration=request.vars.duration,
        rating=0,
        num_plays=0
    )
    t = db.track(t_id)
    return response.json(dict(track=t))


@auth.requires_signature()
def del_track():
    db(db.track.id == request.vars.track_id).delete()
    return "ok"


def _get_artist_id_from_spotify(artist):
    url = "https://api.spotify.com/v1/search"
    params = dict(q=artist, type='artist', limit=1)
    results = requests.get(url=url, params=params)
    result_json = results.json()
    print result_json
    if result_json.has_key('artists'):
        items = result_json['artists']['items']
    else:
        return None
    if len(items):
        return items[0]['id']
    else:
        return None


def _parse_spotify_tracks(results):
    tracks = results['tracks']
    ret_tracks = []
    for track in tracks:
        t = {}
        t['album'] = track['album']['name']
        t['artist'] = track['artists'][0]['name']
        t['title'] = track['name']
        t['duration'] = float(track['duration_ms']) / 1000.0
        t['rating'] = float(track['popularity']) / 100.0
        t['num_plays'] = 0
        t['track_source'] = 'spotify'
        t['track_uri'] = track['uri']
        db.track.insert(**t)

        t['audio_file'] = "https://embed.spotify.com/?uri={}&theme=white".format(t['track_uri'])
        ret_tracks.append(t)
    return ret_tracks


def _get_tracks_from_spotify_for_artist(artist):
    artist_id = _get_artist_id_from_spotify(artist=artist)
    if artist_id is None:
        response.flash = T("Artist '{}' not found".format(artist))
        return []
    country = 'US'
    url = "https://api.spotify.com/v1/artists/{}/top-tracks".format(artist_id)
    params = {}
    params['country'] = country
    results = requests.get(url=url, params=params)
    results_for_db = _parse_spotify_tracks(results.json())
    return results_for_db


@request.restful()
@auth.requires_signature()
def add_track_from_spotify():
    def GET(*args, **vars):
        return dict()

    def POST(*args, **vars):
        artist = vars.get('artist', '')
        tracks = _get_tracks_from_spotify_for_artist(artist=artist)
        if not len(tracks):
            response.flash = T("Could not get tracks. Please check artist name")
        return response.json(dict(tracks_from_spotify=tracks))

    return locals()
