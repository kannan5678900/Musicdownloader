from pyrogram.types import Message
import os
import shutil
from pyrogram import Client, filters
from telegraph import upload_file

TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY",
        "./DOWNLOADS/")

def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj

@Client.on_message(filters.command(["telegraph", "tgm"]))
async def telegraph(client, message):
    msg = await message.reply_text("`processing...`")
    replied = message.reply_to_message
    if not replied:
        await msg.edit("`Please reply to a supported media file...`")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await msg.edit("**Not supported!**")
        return
    t = os.path.join(TMP_DOWNLOAD_DIRECTORY, str(replied.message_id))
    if not os.path.isdir(t):
        os.makedirs(t)
    t += "/"
    download_location = await replied.download(t)
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply_text(text=document)
    else:
        await message.reply_chat_action("typing")
        text = f"**Here Is your Telegraph Link**👇\n\nhttps://telegra.ph{response[0]}" 
        await message.reply_text(text=text, disable_web_page_preview=True, quote=True)
        await msg.delete()
    finally:
        shutil.rmtree(t, ignore_errors=True)
