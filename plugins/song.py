import os
import ffmpeg
import time
import requests
import yt_dlp
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from plugins.google import get_text

@Client.on_message(filters.command(["s", "song", "music"]))
async def song(client, message):
    m = await message.reply('🔎 `Searching for your Song...`')
    query = get_text(message)
    if not query:
        await m.edit("**Give me a song name to download...**\n`/s Believer`")
        return
    print(f"song:{query}")
    chat_id = message.chat.id   
    ydl_opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(alt_title)s.mp3",
            "quiet": True,
            "logtostderr": False,
    }
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]
            thor = results[0]["channel"]          
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            await m.edit('**Found Nothing ❌\nChange the Spelling and try**')
            return
    except Exception as e:
        await m.edit("**Sorry**\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 **Song**.\n\nEg.`/s Believer`")
        print(str(e))
        return
    await m.edit("`Uploading Your Song....Please Wait`🙏\nPlease don't **Spam** me![🥺](https://telegra.ph/file/33e209cb838912e8714c9.mp4)")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        ironman = f'• **Tittle** : __{title}__\n• **Channel** : `{thor}`\n• **Requested For** : `{query}`'
        rep = f"🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : `{duration}`\n👀 𝗩𝗶𝗲𝘄𝘀 : `{views}`\n\n📮 **By** : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n📤 𝗕𝘆 : [Music Downloader 🎶](https://t.me/MusicDownloadv2bot)"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton('sᴇᴀʀᴄʜ ɪɴʟɪɴᴇ', switch_inline_query_current_chat=f'yt ')]])
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await client.send_chat_action(chat_id, "upload_photo")
        await message.reply_photo(thumbnail, caption=ironman, parse_mode='md', ttl_seconds=500)
        await client.send_chat_action(chat_id, "upload_audio")
        await message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=True, title=title, duration=dur, performer=str(info_dict["uploader"]), reply_markup=buttons, thumb=thumb_name)
        await m.delete()
    except Exception as e:
        await m.edit(f'😔**Failed**\n\n__Report this Error to my [Master](https://t.me/Peterparker6)\nOr try__ : `/spotify {query}`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

@Client.on_message(filters.command(["lyrics", "lyric"]))
async def lyrics(_, message):
    msg = await message.reply_text("🔎 **Searching Lyrics....**")
    try:
        if len(message.command) < 2:
            await msg.edit("**Give a lyric name to find.** 😊")
            return
        query = message.text.split(None, 1)[1]
        print(f"lyrics:{query}")
        resp = requests.get(f"https://apis.xditya.me/lyrics?song={query}").json()
        result = f"`{resp['lyrics']}`"
        await message.reply_chat_action("typing")
        await message.reply(result, quote=True)
        await msg.delete()
    except Exception:
        await msg.edit("❌ **lyrics not found.\n\nplease give a valid song name.**")
