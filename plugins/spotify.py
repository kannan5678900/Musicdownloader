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
    download_path = os.getcwd() + "/" + str(uuid.uuid4())
    if not song_link:
        return msg.edit("**Invalid Format ⛔\nEg** : `/spotify Believer`\n\n`/spotify https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP`")
    try:       
        msg.edit(f"`Uploading Your Song From` **Spotify...\nPlease Wait for Some Seconds**[😪](https://telegra.ph/file/2c42b889a0dfb0c24f27a.jpg)")
        spotdl.download_from_spotify(download_path, song_link)
        spotdl.send_songs_from_directory(download_path, client, message)
        try:
            msg.delete()
            print(song_link)
        except Exception as e:
            msg.edit('😔 𝙵𝚊𝚒𝚕𝚎𝚍\n\n𝚁𝚎𝚙𝚘𝚛𝚝 𝚃𝚑𝚒𝚜 𝙴𝚛𝚛𝚘𝚛 𝚝𝚘 𝙵𝚒𝚡 @Peterparker6 🧡')
            print(e)
    except Exception as e:
        msg.edit(f'Failed to download your **Query** - {song_link}')
        print(e)
  
