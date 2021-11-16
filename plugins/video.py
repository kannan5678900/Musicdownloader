import os
import ffmpeg
import time
import requests
import yt_dlp
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(["v", "video", "vsong"]))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    chat_id = message.chat.id
    m = message.reply("`🔎Searching for your Video Song...`")
    ydl_opts = {
        "format": "best/bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
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
            m.edit('**Found Nothing ❌**\nChange the **Spelling** and Try🌝.\n\n`/v Faded`')
            return
    except Exception as e:
        m.edit("𝐒𝐨𝐫𝐫𝐲\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 **Song.\n\nEg.`/v Believer`")
        print(str(e))
        return
    m.edit("__Uploading Your Video....Please Wait__🙏🏻\nPlease don't **Spam** me![🥺](https://telegra.ph/file/988fecf605d9e2caf0a50.mp4)")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : `{duration}`\n👀 𝗩𝗶𝗲𝘄𝘀 : `{views}`\n🍁**Channel** : `{thor}`\n⭕ **Requested For** : `{query}`\n\n📬 **By** : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n📤 𝗕𝘆 : @MusicDownloadv2bot"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton('Search Inline', switch_inline_query_current_chat=f'yt ')]])
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        client.send_chat_action(chat_id, "upload_video")
        message.reply_video(video_file, caption=rep, parse_mode='md',quote=True, duration=dur, reply_markup=buttons, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('😔 **Failed**\n\n`Report this Error to` @Peterparker6 🧑‍💻')
        print(e)
    try:
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
