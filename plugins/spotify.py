import os
import uuid
import ffmpeg
import traceback

from handlers import spotdl

from pyrogram import Client, filters
from pyrogram.types import Message

from plugins.google import get_text

@Client.on_message(filters.command(["spotify"]))
def send_spotify_songs(client, message: Message):
    msg = message.reply_text("`Processing...`")
    song_link = get_text(message)
    chat_id = message.chat.id
    if not song_link:
        return msg.edit("**Invalid Format ⛔\nEg** : `/spotify Believer`\n\n`/spotify https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP`")
    try:
        download_path = os.getcwd() + "/" + str(uuid.uuid4())
    except Exception as e:
        print(e)
        msg.edit(f'**Found Nothing to your Query :** `{song_link}` ❌')
        return
    msg.edit(f"`Uploading Your Song From` **Spotify**...`\n**Please Wait for Some Seconds** [😪](https://telegra.ph/file/1773306efae08a9edfa89.png)")
    spotdl.download_from_spotify(download_path, song_link)
    spotdl.send_songs_from_directory(download_path, client, message)
    msg.delete()
    es = traceback.format_exc()
    print(es)
