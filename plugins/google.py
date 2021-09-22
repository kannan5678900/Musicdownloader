import re
import urllib
import urllib.request

import bs4
import requests
from bs4 import BeautifulSoup
from pyrogram import filters, Client

from search_engine_parser import GoogleSearch


@Client.on_message(filters.command("google") & ~filters.edited)
async def google(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**Give me Something to Search**🤭\n\n`/google Avengers`")
            return
        text = message.text.split(None, 1)[1]
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
