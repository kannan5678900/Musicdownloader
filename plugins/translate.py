from pyrogram import Client, filters
from pyrogram.types import Message
from gpytranslate import Translator

trans = Translator()

@Client.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("**Please reply to a message to translate it!** 😊\n\nSupporting Languages - /lang")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "id"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"👉 <b>Translated from --> {source} to {dest}</b>:\n\n"
        f"📍 <code>{translation.text}</code>\n\n"
        f"@MusicDownloadv2bot"
    )

    await message.reply_text(reply, parse_mode="html", quote=True)

@Client.on_message(filters.command(["lang", "language"]))
async def lang(client, message):
    await message.reply("https://telegra.ph/Music-Downloader-12-20")
