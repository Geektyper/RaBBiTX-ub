from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, exceptions, upload_file

from config import STUFF
from bunny.helpers.basic import edit_or_reply, get_text
from bunny.helpers.tools import *

cmd = STUFF.COMMAND_HANDLER

telegraph = Telegraph()
r = telegraph.create_account(short_name="Userbot")
auth_url = r["auth_url"]


@Client.on_message(filters.command(["tgm", "telegraph"], cmd) & filters.me)
async def uptotelegraph(client: Client, message: Message):
    geek = await edit_or_reply(message, "`Processing . . .`")
    if not message.reply_to_message:
        await geek.edit(
            "**Please Reply to the Message, to Get the Link from Telegraph.**"
        )
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await geek.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        U_done = (
            f"**Successfully uploaded to** [Telegraph](https://telegra.ph/{media_url[0]})"
        )
        await geek.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await geek.edit(f"**ERROR:** `{exc}`")
            return
        wow_graph = f"**Successfully uploaded to** [Telegraph](https://telegra.ph/{response['path']})"
        await geek.edit(wow_graph)