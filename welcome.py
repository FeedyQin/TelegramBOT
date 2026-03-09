from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import mention, terry_wrap
from data.database import get_welcome

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for new_member in update.message.new_chat_members:
        if new_member.is_bot:
            if new_member.id == context.bot.id:
                await update.message.reply_text(
                    terry_wrap("THE TEMPLE IS NOW ONLINE.\nГотов к работе! Дай права администратора и введи /help."),
                    parse_mode=ParseMode.HTML
                )
            continue

        chat = update.effective_chat
        welcome_text = get_welcome(chat.id)

        try:
            formatted = welcome_text.format(
                name=mention(new_member),
                chat=f"<b>{chat.title}</b>",
                username=f"@{new_member.username}" if new_member.username else new_member.first_name,
                id=new_member.id
            )
        except Exception:
            formatted = welcome_text

        try:
            count = await chat.get_member_count()
            footer = f"\n👥 Ты #{count} в этом храме."
        except Exception:
            footer = ""

        await update.message.reply_text(formatted + footer, parse_mode=ParseMode.HTML)

async def farewell_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.left_chat_member
    if user.is_bot:
        return
    await update.message.reply_text(
        terry_wrap(f"👋 {mention(user)} ПОКИНУЛ ХРАМ. THE RECORD IS NOTED."),
        parse_mode=ParseMode.HTML
    )

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if not result:
        return
    was = result.old_chat_member.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR, ChatMember.RESTRICTED]
    is_now = result.new_chat_member.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR, ChatMember.RESTRICTED]
    if not was and is_now:
        user = result.new_chat_member.user
        if not user.is_bot:
            await context.bot.send_message(
                result.chat.id,
                terry_wrap(f"🔥 {mention(user)} ENTERED THE TEMPLE. GOD SEES ALL."),
                parse_mode=ParseMode.HTML
            )
