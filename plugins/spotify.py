import os
import uuid
import ffmpeg
import traceback

from handlers import spotdl

from pyrogram import Client, filters
from pyrogram.types import Message

from plugins.google import get_text

@Client.on_message(filters.command(["spotify", "spot"]))
async def send_spotify_songs(client, message: Message):
    msg = await message.reply_text("`Processing...`")
    song_link = get_text(message)
    user_id = message.from_user.id
    print(f"Spotify:{song_link}.NAME: {message.from_user.mention()}-UserId: {user_id}")
    chat_id = message.chat.id
    download_path = os.getcwd() + "/" + str(uuid.uuid4())
    if not song_link:
        return await msg.edit("**Invalid Format ⛔\nEg** : `/spotify Believer`\n\n`/spotify https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP`")
    if 'https://www.shazam.com/' in song_link:
        return await msg.edit('__Hmm Strange 😑__')
    if "(" in song_link:
        return await msg.edit("Please Remove '( )' and try...")
#    if 'https://youtube.com/' or 'http://www.youtube.com/' in song_link:
#        return msg.edit(f"Are you Kidding me?\n\n`/music {song_link}`")
    try:       
        await msg.edit(f"`Uploading Your Song From` **Spotify...\nPlease Wait for Some Seconds**[😪](https://telegra.ph/file/99dfbd8791044f70db76b.jpg)")
        spotdl.download_from_spotify(download_path, song_link)
        spotdl.send_songs_from_directory(download_path, client, message)
        try:
            await msg.delete()
        except Exception as e:
            await msg.edit('😔 𝙵𝚊𝚒𝚕𝚎𝚍\n\n𝚁𝚎𝚙𝚘𝚛𝚝 𝚃𝚑𝚒𝚜 𝙴𝚛𝚛𝚘𝚛 𝚝𝚘 𝙵𝚒𝚡 @Peterparker6 🧡')
            print(e)
    except Exception as e:
        await msg.edit(f'Failed to download your **Query** - {song_link}')
        print(e)
