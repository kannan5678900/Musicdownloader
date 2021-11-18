from pyrogram import Client, filters

from youtube_search import YoutubeSearch

from plugins.google import get_text

@Client.on_message(filters.command(["yts", "ytsearch"]))
async def yt_search(client, message):
    query = get_text(message)
    if not query:
        return await message.reply_text("`Give me Something to Search in YouTube!`😇")
    try:
        msg = await message.reply("🔎")
        results = YoutubeSearch(query, max_results=10).to_dict()
        i = 0
        text = ""
        while i < 10:
            text += f"🍁 **Name:** __{results[i]['title']}__\n"
            text += f"⏱ **Duration:** `{results[i]['duration']}`\n"
            text += f"👀 **Views:** `{results[i]['views']}`\n"
            text += f"💥 **Channel:** {results[i]['channel']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await message.reply_chat_action("typing")
        await message.reply_text(text=text, disable_web_page_preview=True, quote=True)
        await msg.delete()
    except Exception as e:
        await msg.edit(str(e))
