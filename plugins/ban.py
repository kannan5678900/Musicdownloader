from pyrogram import Client, filters
from handlers.extract_user import extract_user

@Client.on_message(filters.command(["ban"]))
async def ban_user(_, message):
    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"{user_first_name}"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )
        else:
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )
