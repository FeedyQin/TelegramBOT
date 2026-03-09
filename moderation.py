import asyncio
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import BAD_WORDS, ANTIFLOOD_ENABLED, ANTISWEAR_ENABLED, FLOOD_LIMIT, FLOOD_TIME
from data.database import get_flood_data, update_flood, increment_stats
from utils import mention

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not update.effective_chat:
        return
    if update.effective_chat.type == "private":
        return

    user = update.effective_user
    chat = update.effective_chat
    text = message.text or ""

    if user.is_bot:
        return

    increment_stats(chat.id, user.id, "messages")

    try:
        member = await chat.get_member(context.bot.id)
        bot_is_admin = member.status in ["administrator", "creator"]
    except Exception:
        bot_is_admin = False

    if ANTISWEAR_ENABLED and bot_is_admin:
        if any(word in text.lower() for word in BAD_WORDS):
            try:
                await message.delete()
                warn_msg = await context.bot.send_message(
                    chat.id,
                    f"🚫 {mention(user)}, нецензурная лексика запрещена! THE TEMPLE IS PURE.",
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(5)
                await warn_msg.delete()
            except Exception:
                pass
            return

    if ANTIFLOOD_ENABLED and bot_is_admin:
        now = datetime.now()
        flood_data = get_flood_data(chat.id, user.id)
        last_time_str = flood_data.get("last_time")
        count = flood_data.get("count", 0)

        if last_time_str:
            last_time = datetime.fromisoformat(last_time_str)
            count = count + 1 if (now - last_time).total_seconds() <= FLOOD_TIME else 1
        else:
            count = 1

        update_flood(chat.id, user.id, count, now.isoformat())

        if count >= FLOOD_LIMIT:
            update_flood(chat.id, user.id, 0, now.isoformat())
            try:
                await message.delete()
                perms = ChatPermissions(can_send_messages=False)
                await chat.restrict_member(user.id, perms, until_date=now + timedelta(minutes=5))
                flood_msg = await context.bot.send_message(
                    chat.id,
                    f"🌊 {mention(user)} MUTED 5min FOR FLOOD. TEMPLE NOISE CONTROL ACTIVATED.",
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(10)
                await flood_msg.delete()
            except Exception:
                pass
