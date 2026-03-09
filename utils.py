import random
from telegram import Update, Chat, ChatMember
from telegram.ext import ContextTypes
from functools import wraps
from config import TERRY_INTROS, TERRY_OUTROS, TERRY_ERRORS

def mention(user):
    name = user.full_name or user.username or str(user.id)
    return f'<a href="tg://user?id={user.id}">{name}</a>'

def terry_wrap(text):
    intro = random.choice(TERRY_INTROS)
    outro = random.choice(TERRY_OUTROS)
    return f"<b>{intro}</b>\n\n{text}\n\n<i>{outro}</i>"

def terry_error():
    return f"<b>{random.choice(TERRY_ERRORS)}</b>"

def is_admin_check(member):
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

def admin_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        if not update.effective_chat or update.effective_chat.type == Chat.PRIVATE:
            await update.effective_message.reply_text(
                f"<b>GOD SAID:</b> Эта команда только для групп. RING 0 DENIED.",
                parse_mode="HTML"
            )
            return
        member = await update.effective_chat.get_member(update.effective_user.id)
        if not is_admin_check(member):
            await update.effective_message.reply_text(
                f"<b>ACCESS DENIED BY GOD.</b>\nТолько администраторы. THE TEMPLE IS CLOSED TO YOU.",
                parse_mode="HTML"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def bot_admin_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        bot_member = await update.effective_chat.get_member(context.bot.id)
        if not is_admin_check(bot_member):
            await update.effective_message.reply_text(
                "<b>HOLY C COMPILE ERROR:</b> Дай мне права администратора. GOD DEMANDS IT.",
                parse_mode="HTML"
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

async def get_target_user(update, context):
    message = update.effective_message
    target = None
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "Причина не указана"

    if message.reply_to_message:
        target = message.reply_to_message.from_user
        reason = " ".join(context.args) if context.args else "Причина не указана"
    elif context.args:
        username = context.args[0].lstrip("@")
        try:
            if username.isdigit():
                chat_member = await update.effective_chat.get_member(int(username))
            else:
                chat_member = await update.effective_chat.get_member(
                    (await context.bot.get_chat(f"@{username}")).id
                )
            target = chat_member.user
        except Exception:
            return None, None, "Пользователь не найден. GOD DOESN'T KNOW THIS PERSON."

    return target, reason, None

def parse_time(time_str):
    if not time_str:
        return None
    units = {"m": 60, "ч": 3600, "h": 3600, "д": 86400, "d": 86400, "s": 1, "с": 1}
    if time_str[-1] in units:
        try:
            return int(time_str[:-1]) * units[time_str[-1]]
        except ValueError:
            return None
    return None

def format_time(seconds):
    if seconds < 60:
        return f"{seconds}с"
    elif seconds < 3600:
        return f"{seconds // 60}м"
    elif seconds < 86400:
        return f"{seconds // 3600}ч"
    else:
        return f"{seconds // 86400}д"

def get_text_command(text):
    if not text:
        return None, []
    text = text.strip()
    if text.startswith("/"):
        text = text[1:]
    parts = text.split()
    if not parts:
        return None, []
    cmd = parts[0].lower().split("@")[0]
    args = parts[1:]
    return cmd, args
