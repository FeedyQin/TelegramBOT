import re
import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ChatMemberHandler, CallbackQueryHandler
)
from config import BOT_TOKEN
from handlers import admin, fun, moderation, games, welcome
from handlers.aliases import alias_router, COMMAND_ALIASES

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

ALL_ALIASES = []
for canonical, aliases in COMMAND_ALIASES.items():
    ALL_ALIASES.append(canonical)
    ALL_ALIASES.extend(aliases)

ALIAS_PATTERN = re.compile(
    r"^/?(" + "|".join(re.escape(a) for a in sorted(ALL_ALIASES, key=len, reverse=True)) + r")(\s|$|@)",
    re.IGNORECASE
)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", fun.start))
    app.add_handler(CommandHandler("help", fun.help_cmd))
    app.add_handler(CommandHandler("id", fun.get_id))
    app.add_handler(CommandHandler("info", fun.info))
    app.add_handler(CommandHandler("ping", fun.ping))
    app.add_handler(CommandHandler("chatinfo", fun.chatinfo))
    app.add_handler(CommandHandler("stats", fun.stats))
    app.add_handler(CommandHandler("time", fun.time_cmd))

    app.add_handler(CommandHandler("ban", admin.ban))
    app.add_handler(CommandHandler("unban", admin.unban))
    app.add_handler(CommandHandler("kick", admin.kick))
    app.add_handler(CommandHandler("mute", admin.mute))
    app.add_handler(CommandHandler("unmute", admin.unmute))
    app.add_handler(CommandHandler("warn", admin.warn))
    app.add_handler(CommandHandler("unwarn", admin.unwarn))
    app.add_handler(CommandHandler("warns", admin.warns))
    app.add_handler(CommandHandler("purge", admin.purge))
    app.add_handler(CommandHandler("pin", admin.pin))
    app.add_handler(CommandHandler("unpin", admin.unpin))
    app.add_handler(CommandHandler("promote", admin.promote))
    app.add_handler(CommandHandler("demote", admin.demote))
    app.add_handler(CommandHandler("admins", admin.list_admins))
    app.add_handler(CommandHandler("setwelcome", admin.setwelcome))

    app.add_handler(CommandHandler("8ball", fun.eightball))
    app.add_handler(CommandHandler("roll", fun.roll))
    app.add_handler(CommandHandler("flip", fun.flip))
    app.add_handler(CommandHandler("joke", fun.joke))
    app.add_handler(CommandHandler("quote", fun.quote))
    app.add_handler(CommandHandler("cat", fun.cat))
    app.add_handler(CommandHandler("dog", fun.dog))
    app.add_handler(CommandHandler("meme", fun.meme))
    app.add_handler(CommandHandler("rate", fun.rate))
    app.add_handler(CommandHandler("ship", fun.ship))
    app.add_handler(CommandHandler("choose", fun.choose))
    app.add_handler(CommandHandler("calc", fun.calc))
    app.add_handler(CommandHandler("fact", fun.fact))
    app.add_handler(CommandHandler("compliment", fun.compliment))
    app.add_handler(CommandHandler("insult", fun.insult))
    app.add_handler(CommandHandler("bible", fun.bible))
    app.add_handler(CommandHandler("horoscope", fun.horoscope))
    app.add_handler(CommandHandler("password", fun.password))
    app.add_handler(CommandHandler("rps", fun.rps))
    app.add_handler(CommandHandler("slot", fun.slot))
    app.add_handler(CommandHandler("dice", fun.dice))
    app.add_handler(CommandHandler("fortune", fun.fortune))
    app.add_handler(CommandHandler("wyr", fun.wyr))
    app.add_handler(CommandHandler("truth", fun.truth))
    app.add_handler(CommandHandler("dare", fun.dare))
    app.add_handler(CommandHandler("ascii", fun.ascii_art))
    app.add_handler(CommandHandler("note", fun.note))
    app.add_handler(CommandHandler("notes", fun.notes))
    app.add_handler(CommandHandler("get", fun.get_note))
    app.add_handler(CommandHandler("delnote", fun.del_note_cmd))

    app.add_handler(CommandHandler("ttt", games.tictactoe_start))
    app.add_handler(CommandHandler("quiz", games.quiz_start))
    app.add_handler(CommandHandler("trivia", games.trivia))

    app.add_handler(CallbackQueryHandler(games.tictactoe_move, pattern="^ttt_"))
    app.add_handler(CallbackQueryHandler(games.quiz_answer, pattern="^quiz_"))
    app.add_handler(CallbackQueryHandler(fun.wyr_vote, pattern="^wyr_"))

    app.add_handler(ChatMemberHandler(welcome.greet_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.welcome_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, welcome.farewell_message))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(ALIAS_PATTERN),
        alias_router
    ))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, moderation.check_message))

    print("🏛️ TEMPLEOS BOT IS RUNNING. GOD SEES ALL.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
