import re
from telegram import Update
from telegram.ext import ContextTypes
from utils import get_text_command

COMMAND_ALIASES = {
    "start": ["старт", "начало", "начать", "go"],
    "help": ["помощь", "хелп", "команды", "h", "?", "помоги"],
    "ban": ["бан", "забанить", "заблокировать", "block"],
    "unban": ["разбан", "разбанить", "разблокировать", "unblock"],
    "kick": ["кик", "кикнуть", "выгнать", "выкинуть"],
    "mute": ["мут", "замутить", "замолчать", "silence"],
    "unmute": ["размут", "размутить", "голос"],
    "warn": ["варн", "предупреждение", "предупредить", "w"],
    "unwarn": ["снятьварн", "сняварн", "убратьварн", "removewarn", "uw"],
    "warns": ["варны", "предупреждения", "историяварнов", "wl"],
    "purge": ["очистить", "удалить", "чистить", "чистка", "clear"],
    "pin": ["закрепить", "прикрепить", "пин"],
    "unpin": ["открепить", "удалитьзакрепление", "unpin"],
    "promote": ["повысить", "сделатьадмином", "адм", "admin"],
    "demote": ["понизить", "снятьадмина", "убратьадмина"],
    "admins": ["админы", "администраторы", "adminlist", "админы"],
    "setwelcome": ["установитьприветствие", "welcomeset", "setgreet"],
    "8ball": ["шар", "магшар", "предскажи", "ball", "eball"],
    "roll": ["кубик", "бросить", "dice2", "рол"],
    "flip": ["монетка", "монета", "орёл", "решка", "подбросить"],
    "joke": ["анекдот", "шутка", "jokes", "рассмеши", "смешно", "юмор", "хаха"],
    "quote": ["цитата", "мудрость", "умность", "мысль"],
    "ship": ["совместимость", "любовь", "пара", "купидон"],
    "rate": ["оценить", "оценка", "рейтинг", "оцени", "rate"],
    "choose": ["выбор", "выбери", "выбрать", "или", "decide"],
    "calc": ["калькулятор", "посчитай", "расчёт", "math", "матан"],
    "wyr": ["чтолучше", "лучше", "либо", "wouldyourather"],
    "fact": ["факт", "интересно", "знаешьли", "facts"],
    "compliment": ["комплимент", "похвали", "скажинежность"],
    "insult": ["оскорбление", "оскорби", "наругай", "дразни"],
    "bible": ["библия", "слово", "стих", "господь", "бог"],
    "horoscope": ["гороскоп", "звёзды", "знак", "предсказание2"],
    "password": ["пароль", "генпароль", "генератор", "pass"],
    "rps": ["ксо", "ножницыкаменьбумага", "камень", "ножницы", "бумага"],
    "slot": ["слот", "казино", "однорукийбандит", "слоты"],
    "dice": ["кости", "d6", "бросьдайс", "дайс"],
    "fortune": ["судьба", "предскажи2", "будущее", "оракул"],
    "ascii": ["аски", "арт", "asciiart"],
    "truth": ["правда", "честно"],
    "dare": ["действие", "задание", "вызов"],
    "ttt": ["крестикинолики", "крестики", "нолики", "xo", "хо"],
    "quiz": ["викторина", "тест", "тестнаумного", "знатоки"],
    "trivia": ["вопрос", "загадка", "опросник"],
    "id": ["айди", "идентификатор", "whoami", "кто"],
    "info": ["инфо", "информация", "профиль", "profile"],
    "ping": ["пинг", "живой", "жив", "echo"],
    "chatinfo": ["инфочата", "чатинфо", "groupinfo"],
    "stats": ["стата", "статистика", "активность"],
    "time": ["время", "дата", "сейчас", "now"],
    "cat": ["кот", "котик", "кошка", "котята", "мяу"],
    "dog": ["собака", "пёс", "собак", "гав", "doggo"],
    "meme": ["мем", "мемас", "смешнаякартинка", "prикол"],
    "note": ["заметка", "запомни", "сохрани", "remember"],
    "notes": ["заметки", "мойсписок", "список"],
    "get": ["покажи", "показать", "достать", "вспомни"],
    "delnote": ["удзаметку", "удалитьзаметку", "забудь", "delnote"],
}

REVERSE_ALIASES = {}
for canonical, aliases in COMMAND_ALIASES.items():
    for alias in aliases:
        REVERSE_ALIASES[alias.lower()] = canonical
    REVERSE_ALIASES[canonical.lower()] = canonical

async def alias_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    cmd, args = get_text_command(message.text)
    if not cmd:
        return

    canonical = REVERSE_ALIASES.get(cmd.lower())
    if not canonical:
        return

    context.args = args

    from handlers import fun, admin, games

    handlers_map = {
        "start": fun.start,
        "help": fun.help_cmd,
        "id": fun.get_id,
        "info": fun.info,
        "ping": fun.ping,
        "chatinfo": fun.chatinfo,
        "stats": fun.stats,
        "time": fun.time_cmd,
        "8ball": fun.eightball,
        "roll": fun.roll,
        "flip": fun.flip,
        "joke": fun.joke,
        "quote": fun.quote,
        "rate": fun.rate,
        "ship": fun.ship,
        "choose": fun.choose,
        "calc": fun.calc,
        "fact": fun.fact,
        "compliment": fun.compliment,
        "insult": fun.insult,
        "bible": fun.bible,
        "horoscope": fun.horoscope,
        "password": fun.password,
        "rps": fun.rps,
        "slot": fun.slot,
        "dice": fun.dice,
        "fortune": fun.fortune,
        "wyr": fun.wyr,
        "truth": fun.truth,
        "dare": fun.dare,
        "ascii": fun.ascii_art,
        "cat": fun.cat,
        "dog": fun.dog,
        "meme": fun.meme,
        "note": fun.note,
        "notes": fun.notes,
        "get": fun.get_note,
        "delnote": fun.del_note_cmd,
        "ban": admin.ban,
        "unban": admin.unban,
        "kick": admin.kick,
        "mute": admin.mute,
        "unmute": admin.unmute,
        "warn": admin.warn,
        "unwarn": admin.unwarn,
        "warns": admin.warns,
        "purge": admin.purge,
        "pin": admin.pin,
        "unpin": admin.unpin,
        "promote": admin.promote,
        "demote": admin.demote,
        "admins": admin.list_admins,
        "setwelcome": admin.setwelcome,
        "ttt": games.tictactoe_start,
        "quiz": games.quiz_start,
        "trivia": games.trivia,
    }

    handler = handlers_map.get(canonical)
    if handler:
        await handler(update, context)
