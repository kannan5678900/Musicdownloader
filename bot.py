from pyrogram import Client
import pyromod.listen
import os
from os import path
from shazamio import Shazam, exceptions, FactoryArtist, FactoryTrack

shazam = Shazam()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "6"))
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    bot = Client(
        "Music-Bot",
        bot_token=BOT_TOKEN,
        api_hash=API_HASH,
        api_id=API_ID,
        plugins=plugins
    )
    bot.run()

class bot(Client):
    
    async def recognize(self, path):
        return await shazam.recognize_song(path)

    async def related(self, track_id):
        try:
            return (await shazam.related_tracks(track_id=track_id, limit=50, start_from=2))['tracks']
        except exceptions.FailedDecodeJson:
            return None
    
    async def get_artist(self, query: str):
        artists = await shazam.search_artist(query=query, limit=50)
        hits = []
        try:
            for artist in artists['artists']['hits']:
                hits.append(FactoryArtist(artist).serializer())
            return hits
        except KeyError:
            return None
        
    async def get_artist_tracks(self, artist_id: int):
        tracks = []
        tem = (await shazam.artist_top_tracks(artist_id=artist_id, limit=50))['tracks']
        try:
            for track in tem:
                tracks.append(FactoryTrack(data=track).serializer())
            return tracks
        except KeyError:
            return None
