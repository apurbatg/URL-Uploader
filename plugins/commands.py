# 🖤💗 Developede by @LISA_FAN_LK | @UploadLinkToFileBot


import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.translation import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.add import add_user_to_database
from functions.forcesub import handle_force_subscribe
from plugins.database.database import  insert ,find_one

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    await add_user_to_database(bot, update)
    await bot.send_message(
        Config.LOG_CHANNEL,
           f"#NEW_USER: \n\nNew User [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )
    await bot.send_chat_action(
       chat_id=update.chat.id,
       action="typing"
    )
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )

@Client.on_message(filters.private &( filters.document | filters.audio | filters.video | filters.regex(pattern=".*http.*")))
async def send_doc(client,message):
       update_channel = Config.UPDATE_CHANNEL
       user_id = message.from_user.id
       if update_channel :
       	try:
       		await client.get_chat_member(update_channel, user_id)
       	except UserNotParticipant:
       		await message.reply_text("Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ!\n\nDᴜᴇ ᴛᴏ Oᴠᴇʀʟᴏᴀᴅ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs Cᴀɴ Usᴇ Mᴇ!",reply_to_message_id = message.message_id, reply_markup = InlineKeyboardMarkup([ [ InlineKeyboardButton("🔰 Jᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ 🔰" ,url=f"https://t.me/{Config.UPDATE_CHANNEL}") ]   ]))
       		return
       date = message.date
       _used_date = find_one(user_id)
       used_date = _used_date["date"]      
       c_time = time.time()
       LIMIT = 240
       then = used_date+ LIMIT
       left = round(then - c_time)
       conversion = datetime.timedelta(seconds=left)
       ltime = str(conversion)
       if left > 0:
       	await app.send_chat_action(message.chat.id, "typing")
       	await message.reply_text(f"```Sorry Dude I am not only for YOU \n Flood control is active so please wait for {ltime}```",reply_to_message_id = message.message_id)
       else:
       	
       	media = await client.get_messages(message.chat.id,message.message_id)
       	file = media.document or media.video or media.audio 
       	dcid = FileId.decode(file.file_id).dc_id
       	filename = file.file_name
       	filesize = humanize.naturalsize(file.file_size)
       	fileid = file.file_id
       	await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid} """,reply_to_message_id = message.message_id,reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),InlineKeyboardButton("✖️ Cancel",callback_data = "cancel")  ]]))

