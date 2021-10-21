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
        return msg.edit("**Invalid Format ⛔\nEg** : `/spotify Believer`")
    try:
        download_path = os.getcwd() + "/" + str(uuid.uuid4())
    except Exception as e:
        print(e)
        msg.edit(f'**Found Nothing to your Query :** `{song_link}` ❌')
        return
    msg.edit(f"`Uploading Your Song From` **Spotify**...\n__Please Wait for Some Seconds__[😪](https://telegra.ph/file/1773306efae08a9edfa89.jpg)")
    spotdl.download_from_spotify(download_path, song_link)
    spotdl.send_songs_from_directory(download_path, client, message)
    msg.delete()
    es = traceback.format_exc()
    print(es)