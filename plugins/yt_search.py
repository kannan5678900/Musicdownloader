from pyrogram import Client, filters

from youtubesearchpython import SearchVideos

from plugins.google import get_text

async def ytsearch(query, limit):
    result = ""
    videolinks = SearchVideos(query.lower(), max_results=limit, offset=1, mode="dict")
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += f"**Description : **`{v['descriptionSnippet'][-1]['text']}`\n"
        except Exception:
            textresult += "**Description : **`None`\n"
        textresult += f"**Duration : **__{v['duration']}__  **Views : **__{v['viewCount']['short']}__\n"
        result += f"☞ {textresult}\n"
    return result

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
            text += f"🏷 **Name:** __{results[i]['title']}__\n"
            text += f"⏱ **Duration:** `{results[i]['duration']}`\n"
            text += f"👀 **Views:** `{results[i]['views']}`\n"
            text += f"📣 **Channel:** {results[i]['channel']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await message.reply_chat_action("typing")
        await message.reply_text(text=text, disable_web_page_preview=True, quote=True)
        await msg.delete()
    except Exception as e:
        await msg.edit(str(e))
