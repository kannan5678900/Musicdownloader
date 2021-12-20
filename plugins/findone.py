import os
from pyrogram import Client ,filters
from handlers.check_user import find_one
import config

ADMIN = config.AUTH_USERS


@Client.on_message(filters.user(ADMIN) & filters.command(["find"]))
async def findmenb(bot, message):
		id = message.text.split("/find")
		user_id = id[1].replace(" ", "")
		await message.reply_text(find_one(int(user_id)))
