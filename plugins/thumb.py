import ytthumb
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("thumb"))
async def send_thumbnail(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("__Please Reply to any YouTube Link or Code...__🙏")
    if not message.reply_to_message.text:
        return await message.reply_text("`This is not YT link/code...`😪😡")
    chat_id = message.chat.id
    m = await message.reply_text("`Downloading...`")
    video = message.reply_to_message.text
    try:
        quality = "maxres"
        thumbnail = ytthumb.thumbnail(video=video, quality=quality)
        caption = f"📤 **@Musicdownloadv2bot**"
        await client.send_chat_action(chat_id, "upload_photo")
        await message.reply_photo(photo=thumbnail, quote=True, caption=caption) 
        await m.delete()
    except Exception as error:
        await m.edit_text(text=error, disable_web_page_preview=True)
