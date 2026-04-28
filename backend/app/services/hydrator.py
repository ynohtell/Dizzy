import os
import time
import requests
import spotipy

from typing import List
from spotipy.oauth2 import SpotifyOAuth

from ..models import Song


# -----------------------------------------
# Lazy Spotify Client
# -----------------------------------------

_sp = None


def get_spotify_client():
    global _sp

    if _sp is None:
        _sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                scope="user-read-recently-played user-top-read user-library-read",
                open_browser=False,
            )
        )

    return _sp


# -----------------------------------------
# Apple Metadata Lookup
# -----------------------------------------

def get_apple_metadata(artist: str, title: str) -> dict:
    try:
        query = f"{artist} {title}"

        res = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": query,
                "media": "music",
                "entity": "song",
                "limit": 1,
                "country": "PH",
            },
            timeout=5,
        )

        if res.status_code == 200:
            results = res.json().get("results", [])
            return results[0] if results else {}

    except Exception as e:
        print(f"⚠️ Apple lookup failed: {artist} - {title} | {e}")

    return {}


# -----------------------------------------
# Full Hydration
# -----------------------------------------

def hydrate_session_songs(raw_songs: list) -> List[Song]:
    if not raw_songs:
        return []

    sp = get_spotify_client()

    spotify_ids = [song["id"] for song in raw_songs if song.get("id")]
    sp_results = sp.tracks(spotify_ids)["tracks"]

    sp_map = {
        track["id"]: track
        for track in sp_results
        if track
    }

    hydrated = []

    for song_data in raw_songs:
        s_id = song_data["id"]
        sp_meta = sp_map.get(s_id)

        if not sp_meta:
            continue

        artist = song_data["artist"]
        title = song_data["title"]

        apple = get_apple_metadata(artist, title)

        song = Song(
            id=s_id,
            title=title,
            artist=artist,
            spotify_id=s_id,

            apple_music_id=str(apple.get("trackId")) if apple else None,
            artwork_url=apple.get("artworkUrl100") if apple else None,
            preview_url=apple.get("previewUrl") if apple else None,
            genre=apple.get("primaryGenreName") if apple else None,

            album_name=sp_meta["album"]["name"],
            year=int(sp_meta["album"]["release_date"][:4]),

            rating=song_data.get("rating", 1000),
            wins=song_data.get("wins", 0),
            losses=song_data.get("losses", 0),
        )

        hydrated.append(song)
        time.sleep(0.1)

    return hydrated


# -----------------------------------------
# Upgrade Existing Sessions (Apple only)
# -----------------------------------------

def upgrade_existing_songs(raw_songs: list) -> List[Song]:
    upgraded = []

    for song_data in raw_songs:
        # 1. Create a copy so we don't mess up the original list
        data = song_data.copy()
        
        artist = data.get("artist")
        title = data.get("title")

        # 2. Get Apple metadata
        apple = get_apple_metadata(artist, title)

        # 3. Update the dictionary only if the fields are missing/null
        # This avoids the "multiple values" error
        if not data.get("apple_music_id") and apple:
            data["apple_music_id"] = str(apple.get("trackId"))
            
        if not data.get("artwork_url") and apple:
            data["artwork_url"] = apple.get("artworkUrl100")
            
        if not data.get("preview_url") and apple:
            data["preview_url"] = apple.get("previewUrl")
            
        if not data.get("genre") and apple:
            data["genre"] = apple.get("primaryGenreName")

        # 4. Now unpack the cleaned dictionary into the model
        try:
            song = Song(**data)
            upgraded.append(song)
        except Exception as e:
            print(f"⚠️ Validation failed for {title}: {e}")
            
        time.sleep(0.1)

    return upgraded