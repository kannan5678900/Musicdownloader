import time
import os
from json import JSONDecodeError
import requests
import ffmpeg
from pyrogram import filters, Client

async def fetch_audio(client, message):
    time.time()
    if not message.reply_to_message:
        await message.reply("`Reply To A Video / Audio.`")
        return
    warner_stark = message.reply_to_message
    if warner_stark.audio is None and warner_stark.video is None:
        await message.reply("`Format Not Supported`😕")
        return
    if warner_stark.video:
        lel = await message.reply("`Video Detected, Converting To Audio !🔥`")
        warner_bros = await message.reply_to_message.download()
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        lel = await edit_or_reply(message, "`Download Started !`")
        final_warner = await message.reply_to_message.download()
    await lel.edit("`Almost Done!🔥`")
    await lel.delete()
    return final_warner

async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


@Client.on_message(filters.command(["shazam"]))
async def shazamm(client, message):
    chat_id = message.chat.id
    thor = await edit_or_reply(message, "`Shazaming In Progress!😑`")
    if not message.reply_to_message:
        await thor.edit("**Reply To Any Audio.**😏😡")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "sucess":false))}
    await thor.edit("**Searching For This Song In Friday's DataBase.**\n__Please Wait..__")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await thor.edit("`Seems Like Our Server Has Some Issues, Please Try Again Later!`")
        return
    if xo.get("success") is False:
        await thor.edit("`Song Not Found IN Database. Please Try Again.`🥲")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    zzz.get("sections")[3]
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b>Song Shazamed</b>
<b>Song Name</b> : <code>{title}</code>
<b>Song By</b> : <code>{by}</code>
<b>Identified By</b> : @MusicDownloadv2bot
"""
    await client.send_chat_action(chat_id, "upload_photo")
    await client.send_photo(message.chat.id, image, messageo, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await thor.delete()
