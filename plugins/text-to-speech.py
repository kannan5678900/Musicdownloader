import traceback
from asyncio import get_running_loop
from io import BytesIO

from googletrans import Translator
from gtts import gTTS
from pyrogram import filters, Client
from pyrogram.types import Message


def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@Client.on_message(filters.command("tts"))
async def text_to_speech(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("`Please Reply to Some Text...`✌️")
    if not message.reply_to_message.text:
        return await message.reply_text("`This is Not Text Message...`😡")
    chat_id = message.chat.id
    m = await message.reply_text("`Converting to Speech...`")
    text = message.reply_to_message.text
    caption = f"**Identified by** : @Musicdownloadv2bot"
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await client.send_chat_action(chat_id, "upload_audio")
        await message.reply_audio(audio, performer='Musicdownloadv2bot', caption=caption)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(str(e))
        es = traceback.format_exc()
        print(es)
