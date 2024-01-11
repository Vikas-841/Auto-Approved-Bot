from os import environ
import re
import logging
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from config import API_ID, API_HASH, ADMINS, DB_NAME
from config import DB_URI as MONGO_URL

pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"]
)

CHAT_ID = [int(pr0fess0r_99) for pr0fess0r_99 in environ.get("CHAT_ID", None).split()]
TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

mongo_client = MongoClient(environ["MONGO_URL"])
mongo_db = mongo_client["cloned_vjbotz"]
mongo_collection = mongo_db[environ["DB_NAME"]]

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: pr0fess0r_99, message: Message):
    approvedbot = await client.get_me() 
    button = [[InlineKeyboardButton("📦 Repo", url="https://github.com/PR0FESS0R-99/Auto-Approved-Bot"), InlineKeyboardButton("Updates 📢", url="t.me/Mo_Tech_YT")],
              [InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"http://t.me/{approvedbot.username}?startgroup=botstart")]]
    await client.send_message(chat_id=message.chat.id, text=f"**__Hello {message.from_user.mention} Iam Auto Approver Join Request Bot Just [Add Me To Your Group Channnl](http://t.me/{approvedbot.username}?startgroup=botstart) || Repo https://github.com/PR0FESS0R-99/Auto-Approved-Bot||**__", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@pr0fess0r_99.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat = message.chat  # Chat
    user = message.from_user  # User
    print(f"{user.first_name} Joined 🤝")  # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=chat.id, text=TEXT.format(mention=user.mention, title=chat.title))

@pr0fess0r_99.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    await message.reply_text(script.CLONE_TXT)

@pr0fess0r_99.on_message((filters.regex(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
async def on_clone(client, message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)
        bots = list(mongo_db.bots.find())
        bot_tokens = None  # Initialize bot_tokens variable

        for bot in bots:
            bot_tokens = bot['token']

        forward_from_id = message.forward_from.id if message.forward_from else None
        if bot_tokens == bot_token and forward_from_id == 93372553:
            await message.reply_text("**©️ ᴛʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ʙᴀʙʏ 🐥**")
            return

        if not forward_from_id != 93372553:
            msg = await message.reply_text("**👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️**")
            try:
                ai = Client(
                    f"{bot_token}", environ["API_ID"], environ["API_HASH"],
                    bot_token=bot_token,
                    plugins={"root": "clone_plugins"},
                )

                await ai.start()
                bot = await ai.get_me()
                details = {
                    'bot_id': bot.id,
                    'is_bot': True,
                    'user_id': user_id,
                    'name': bot.first_name,
                    'token': bot_token,
                    'username': bot.username
                }
                mongo_db.bots.insert_one(details)
                await msg.edit_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sᴇᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ɪɴ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ sᴛᴀʀᴛ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ</b>")
            except BaseException as e:
                logging.exception("Error while cloning bot.")
                await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @KingVJ01 to get assistance.**")
    except Exception as e:
        logging.exception("Error while handling message.")

@pr0fess0r_99.on_message(filters.command("deletecloned") & filters.private)
async def delete_cloned_bot(client, message):
    try:
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)

        mongo_collection = mongo_db.bots

        cloned_bot = mongo_collection.find_one({"token": bot_token})
        if cloned_bot:
            mongo_collection.delete_one({"token": bot_token})
            await message.reply_text("**🤖 ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʟɪsᴛ ᴀɴᴅ ɪᴛs ᴅᴇᴛᴀɪʟs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ. ☠️**")
        else:
            await message.reply_text("**⚠️ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴘʀᴏᴠɪᴅᴇᴅ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪsᴛ.**")
    except Exception as e:
        logging.exception("Error while deleting cloned bot.")
        await message.reply_text("An error occurred while deleting the cloned bot.")

async def restart_bots():
    logging.info("Restarting all bots........")
    bots = list(mongo_db.bots.find())
    for bot in bots:
        bot_token = bot['token']
        try:
            ai = Client(
                f"{bot_token}", environ["API_ID"], environ["API_HASH"],
                bot_token=bot_token,
                plugins={"root": "clone_plugins"},
            )
            await ai.start()
        except Exception as e:
            logging.exception(f"Error while restarting bot with token {bot_token}: {e}")

print("Auto Approved Bot")
pr0fess0r_99.run()
