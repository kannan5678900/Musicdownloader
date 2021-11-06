import os
import traceback
import logging
import asyncio
from time import time
from datetime import datetime
from pyrogram import Client
from pyrogram import StopPropagation, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from handlers.broadcast import broadcast
from handlers.check_user import handle_user_status
from handlers.database import Database

LOG_CHANNEL = config.LOG_CHANNEL
AUTH_USERS = config.AUTH_USERS
DB_URL = config.DB_URL
DB_NAME = config.DB_NAME

db = Database(DB_URL, DB_NAME)

# --------------------------------------------------------------------------------------------------------------------------------------

Help_text = """<u>🌟**Available Commands**</u>

⚡/spotify - **To Download Songs from Spotify.🔥\nEg** : `/spotify Faded`

⚡/s - **To Download Audio Songs from YouTube(Fastest method).💞\nEg** : `/s Believer`

⚡/v - **To Download Best Video Songs(Under 100Mb).🎦\nEg** : `/v Believer`

⚡/tts - **To Convert text to Speech.🔊**

⚡/shazam - **To Search about replied Audio.💨**.

⚡/thumb - **To Download YouTube Thumbnail.📂**

⚡/anime - **To Search about Given Animes.🎭**\n`/anime Avengers`

⚡/google - **To Search Given Query in Google.🔎**\n`/google Avengers`"""

# -------------------------------------------------------------------------------------------------------------------------------------

@Client.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "source":
        await update.answer(
            text="I am Extremely Sorry 😔\nThe Repo have Some Problems now,It will be updated in a month or two.💝",
            show_alert=True
        )
    elif update.data == "close":
        await update.message.delete()

@Client.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@Client.on_message(filters.command("start") & filters.private)
async def startprivate(client, message):
    # return
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        await client.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    joinButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Developer🤠", url="https://t.me/Peterparker6"),
                InlineKeyboardButton("Source😪", callback_data="source")
            ],
            [
                InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
            ]
        ]
    )
    sticker = await client.send_sticker(chat_id, "CAACAgIAAxkBAAEDKoVheSlcqbEDq52yuEH2TqqiPe0ROgACNQEAAjDUnRG0uDX9ZqC2fCEE")
    welcomed = f"👋 𝗛𝗲𝗹𝗹𝗼 **{message.from_user.mention()}**\n\n<b>I am a Advanced Music Downloader With many Features</b>[🤩](https://telegra.ph/file/92a1f08c6ca91e0e8c163.mp4)\n\n𝑺𝒆𝒏𝒕 𝒕𝒉𝒆 𝑵𝒂𝒎𝒆 𝒐𝒇 𝒕𝒉𝒆 𝐒𝐨𝐧𝐠 𝒀𝒐𝒖 𝑾𝒂𝒏𝒕... 😍🥰🤗\n\n<b>I Also Support Inline YouTube Search.</b>\n\n<i>Check</i> /help <i>For More info©.</i>"
    await message.reply_text(welcomed, reply_markup=joinButton, quote=True)
    await asyncio.sleep(60)
    await sticker.delete()
    raise StopPropagation

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
        return
    await broadcast(m, db)

@Client.on_message(filters.private & filters.command("stats"))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Total Users in Database 📂:** `{await db.total_users_count()}`\n\n**Total Users with Notification Enabled 🔔 :** `{await db.total_notif_users_count()}`",
        parse_mode="Markdown",
        quote=True,
    )


@Client.on_message(filters.private & filters.command("ban_user"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@Client.on_message(filters.private & filters.command("unban_user"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@Client.on_message(filters.private & filters.command("banned_users"))
async def _banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **User_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)

    return

@Client.on_message(filters.command(['help']))
async def help(client, message):
       Help_buttons = InlineKeyboardMarkup([[InlineKeyboardButton('Close❌', callback_data="close")]])
       await message.reply_text(text=Help_text, reply_markup=Help_buttons, quote=True)

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply(f"🍁<b>Name</b> : `Music Downloader`\n\n🧑‍💻<b>Developer</b> : [Peter Parker](https://t.me/Peterparker6)\n\n📝<b>Language</b> : `Python3`\n\n💎<b>Server</b> : [Heroku](https://heroku.com/)\n\n♎<b>Library</b> : [Pyrogram](https://docs.pyrogram.org/)\n\n💨<b>Build Stats</b> : `V3.0 [Stable]`\n\n⭕<b>Source Code</b> : [🤥Click here](https://github.com)",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Close🚫', callback_data="close")
                ]
            ]
        )
   )

@Client.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    copy = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await copy.edit_text(
        "🔥 `PONG!!`\n"
        f"💛 `{delta_ping * 1000:.3f} ms`"
    )

@Client.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "⭕ Bot status:\n\n"
        f"• **Uptime:** `{uptime}`\n\n"
        f"• **Start time:** `{START_TIME_ISO}`"
    )   

@Client.on_message(filters.command("rate"))
async def rate(client, message):
       chat_id = message.from_user.id
       Button = InlineKeyboardMarkup(
           [[
           InlineKeyboardButton('Rate Me 🌟', url='https://t.me/tlgrmcbot?start=musicdownloadv2bot-review'),
           InlineKeyboardButton('❌', callback_data="close")
           ]]
       )
       Message = f"**I am very Happy to Hear That! 🥰\n\nThis will be an inspiration to my master😀\nRate me [Here](https://t.me/tlgrmcbot?start=musicdownloadv2bot-review)**"
       stick = await client.send_sticker(chat_id, "CAACAgIAAxkBAAEDIhhhc3nFJpcZErvurFbr5RO6TubSnwACSgEAAjDUnRHtmqasW02BTSEE")
       await message.reply_text(text=Message, reply_markup=Button)
       await asyncio.sleep(30)
       await stick.delete()
