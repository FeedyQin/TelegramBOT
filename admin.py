import asyncio
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest
from utils import admin_required, bot_admin_required, get_target_user, mention, parse_time, format_time, terry_wrap, terry_error
from data.database import get_warns, add_warn, remove_warn, clear_warns
from config import MAX_WARNS

@admin_required
@bot_admin_required
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, reason, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        await update.effective_chat.ban_member(target.id)
        await update.effective_message.reply_text(
            terry_wrap(
                f"🔨 <b>BANNED. GOD JUDGED.</b>\n\n"
                f"👤 {mention(target)}\n"
                f"📋 Причина: {reason}\n"
                f"👮 {mention(update.effective_user)}"
            ),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ DIVINE ERROR: {e}"), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        await update.effective_chat.unban_member(target.id)
        await update.effective_message.reply_text(
            terry_wrap(f"✅ <b>UNBANNED. GOD IS MERCIFUL.</b>\n👤 {mention(target)}"),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, reason, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        await update.effective_chat.ban_member(target.id)
        await update.effective_chat.unban_member(target.id)
        await update.effective_message.reply_text(
            terry_wrap(
                f"👟 <b>KICKED FROM THE TEMPLE.</b>\n\n"
                f"👤 {mention(target)}\n"
                f"📋 Причина: {reason}"
            ),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, reason, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return

    duration = None
    time_str = context.args[-1] if context.args else None
    if time_str:
        secs = parse_time(time_str)
        if secs:
            duration = datetime.now() + timedelta(seconds=secs)
            reason = " ".join(context.args[:-1]) if len(context.args) > 1 else "Причина не указана"

    try:
        perms = ChatPermissions(
            can_send_messages=False, can_send_polls=False,
            can_send_other_messages=False, can_add_web_page_previews=False
        )
        await update.effective_chat.restrict_member(target.id, perms, until_date=duration)
        dur_text = f"⏱ {format_time(int((duration - datetime.now()).total_seconds()))}" if duration else "⏱ НАВСЕГДА."
        await update.effective_message.reply_text(
            terry_wrap(
                f"🔇 <b>MUTED. TEMPLE SILENCE ENFORCED.</b>\n\n"
                f"👤 {mention(target)}\n📋 {reason}\n{dur_text}"
            ),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        perms = ChatPermissions(
            can_send_messages=True, can_send_polls=True,
            can_send_other_messages=True, can_add_web_page_previews=True,
            can_invite_users=True
        )
        await update.effective_chat.restrict_member(target.id, perms)
        await update.effective_message.reply_text(
            terry_wrap(f"🔊 <b>UNMUTED. GOD GRANTS VOICE AGAIN.</b>\n👤 {mention(target)}"),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

@admin_required
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, reason, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return

    chat_id = update.effective_chat.id
    count = add_warn(chat_id, target.id, reason, update.effective_user.full_name)

    if count >= MAX_WARNS:
        await update.effective_chat.ban_member(target.id)
        clear_warns(chat_id, target.id)
        await update.effective_message.reply_text(
            terry_wrap(
                f"🚫 <b>AUTO-BAN EXECUTED. GOD'S JUSTICE.</b>\n\n"
                f"{mention(target)} набрал {MAX_WARNS}/{MAX_WARNS} предупреждений.\n"
                f"📋 Последнее: {reason}"
            ),
            parse_mode=ParseMode.HTML
        )
    else:
        bar = "⚠️" * count + "⬜" * (MAX_WARNS - count)
        await update.effective_message.reply_text(
            terry_wrap(
                f"⚠️ <b>WARNING ISSUED. GOD NOTED.</b>\n\n"
                f"👤 {mention(target)}\n📋 {reason}\n"
                f"📊 {bar} ({count}/{MAX_WARNS})"
            ),
            parse_mode=ParseMode.HTML
        )

@admin_required
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    count = remove_warn(update.effective_chat.id, target.id)
    await update.effective_message.reply_text(
        terry_wrap(f"✅ ПРЕДУПРЕЖДЕНИЕ СНЯТО. GOD IS MERCIFUL.\n👤 {mention(target)}\n📊 Осталось: {count}/{MAX_WARNS}"),
        parse_mode=ParseMode.HTML
    )

async def warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, _ = await get_target_user(update, context)
    if not target:
        target = update.effective_user
    warn_list = get_warns(update.effective_chat.id, target.id)
    if not warn_list:
        await update.effective_message.reply_text(
            terry_wrap(f"✅ {mention(target)} ЧИСТ. GOD APPROVES."),
            parse_mode=ParseMode.HTML
        )
        return
    text = f"⚠️ <b>DIVINE WARN RECORD: {mention(target)}</b>\n\n"
    for i, w in enumerate(warn_list, 1):
        text += f"{i}. {w['reason']} — <i>{w.get('by', '?')}</i>\n"
    text += f"\n📊 {len(warn_list)}/{MAX_WARNS}"
    await update.effective_message.reply_text(terry_wrap(text), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.effective_message.reply_text(terry_wrap("❌ ОТВЕТЬ НА СООБЩЕНИЕ С КОТОРОГО НАЧАТЬ PURGE."), parse_mode=ParseMode.HTML)
        return
    start_id = update.message.reply_to_message.message_id
    end_id = update.message.message_id
    message_ids = list(range(start_id, end_id + 1))
    deleted = 0
    for i in range(0, len(message_ids), 100):
        chunk = message_ids[i:i+100]
        try:
            await context.bot.delete_messages(update.effective_chat.id, chunk)
            deleted += len(chunk)
        except Exception:
            for msg_id in chunk:
                try:
                    await context.bot.delete_message(update.effective_chat.id, msg_id)
                    deleted += 1
                except Exception:
                    pass
    msg = await context.bot.send_message(
        update.effective_chat.id,
        terry_wrap(f"🗑️ PURGED {deleted} MESSAGES. TEMPLE IS CLEAN."),
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except Exception:
        pass

@admin_required
@bot_admin_required
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.effective_message.reply_text(terry_wrap("❌ ОТВЕТЬ НА СООБЩЕНИЕ ДЛЯ ЗАКРЕПЛЕНИЯ."), parse_mode=ParseMode.HTML)
        return
    loud = "--loud" in (context.args or []) or "громко" in (context.args or [])
    await update.message.reply_to_message.pin(disable_notification=not loud)
    await update.effective_message.reply_text(terry_wrap("📌 PINNED. THE TEMPLE SPEAKS."), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.effective_chat.unpin_message()
        await update.effective_message.reply_text(terry_wrap("📌 UNPINNED. TEMPLE SCROLL UPDATED."), parse_mode=ParseMode.HTML)
    except BadRequest:
        await update.effective_message.reply_text(terry_wrap("❌ НЕТ ЗАКРЕПЛЁННЫХ. VOID."), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        await update.effective_chat.promote_member(
            target.id, can_delete_messages=True, can_restrict_members=True,
            can_pin_messages=True, can_invite_users=True,
            can_manage_chat=True, can_manage_video_chats=True
        )
        await update.effective_message.reply_text(
            terry_wrap(f"⭐ {mention(target)} PROMOTED. GOD CHOSE THIS ONE."),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

@admin_required
@bot_admin_required
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, _, error = await get_target_user(update, context)
    if error:
        await update.effective_message.reply_text(terry_wrap(f"❌ {error}"), parse_mode=ParseMode.HTML)
        return
    if not target:
        await update.effective_message.reply_text(terry_wrap("❌ УКАЖИ ПОЛЬЗОВАТЕЛЯ."), parse_mode=ParseMode.HTML)
        return
    try:
        await update.effective_chat.promote_member(
            target.id, can_delete_messages=False, can_restrict_members=False,
            can_pin_messages=False, can_invite_users=False, can_manage_chat=False
        )
        await update.effective_message.reply_text(
            terry_wrap(f"🔻 {mention(target)} DEMOTED. GOD TAKETH AWAY."),
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        await update.effective_message.reply_text(terry_wrap(f"❌ {e}"), parse_mode=ParseMode.HTML)

async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await update.effective_chat.get_administrators()
    text = "👮 <b>DIVINE ADMIN LIST:</b>\n\n"
    for i, admin in enumerate(admins, 1):
        if admin.user.is_bot:
            continue
        role = "👑 Владелец" if admin.status == "creator" else "⭐ Администратор"
        text += f"{i}. {mention(admin.user)} — {role}\n"
    await update.effective_message.reply_text(terry_wrap(text), parse_mode=ParseMode.HTML)

@admin_required
async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data.database import set_welcome
    if not context.args:
        await update.effective_message.reply_text(
            terry_wrap("❓ /setwelcome {name} ТЕКСТ\n\nДоступные переменные:\n{name} — имя\n{chat} — название чата"),
            parse_mode=ParseMode.HTML
        )
        return
    text = " ".join(context.args)
    set_welcome(update.effective_chat.id, text)
    await update.effective_message.reply_text(terry_wrap("✅ WELCOME-СООБЩЕНИЕ УСТАНОВЛЕНО. TEMPLE UPDATED."), parse_mode=ParseMode.HTML)
