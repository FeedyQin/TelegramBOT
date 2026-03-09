import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import terry_wrap

TRIVIA_QUESTIONS = [
    {"q": "Самая большая планета Солнечной системы?", "options": ["Сатурн", "Юпитер", "Нептун", "Уран"], "answer": 1},
    {"q": "Год изобретения World Wide Web?", "options": ["1969", "1983", "1991", "1999"], "answer": 2},
    {"q": "Кто написал «Война и мир»?", "options": ["Достоевский", "Пушкин", "Чехов", "Толстой"], "answer": 3},
    {"q": "Сколько цветов в радуге?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"q": "Самая большая страна по площади?", "options": ["США", "Китай", "Россия", "Канада"], "answer": 2},
    {"q": "Сколько костей в теле взрослого?", "options": ["186", "206", "226", "246"], "answer": 1},
    {"q": "Кто создал Python?", "options": ["Торвальдс", "Страуструп", "ван Россум", "Кёрниган"], "answer": 2},
    {"q": "В каком городе Эйфелева башня?", "options": ["Лондон", "Берлин", "Рим", "Париж"], "answer": 3},
    {"q": "Что означает HTML?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Meta Language", "Hyper Transfer Markup Logic"], "answer": 0},
    {"q": "Сколько байт в одном килобайте?", "options": ["512", "1000", "1024", "2048"], "answer": 2},
    {"q": "Кто написал TempleOS?", "options": ["Линус Торвальдс", "Ричард Столлман", "Терри Дэвис", "Билл Гейтс"], "answer": 2},
    {"q": "На каком языке написана TempleOS?", "options": ["C", "Assembly", "Holy C", "Pascal"], "answer": 2},
    {"q": "Что такое NULL?", "options": ["Ноль", "Пустая строка", "Отсутствие значения", "Ошибка"], "answer": 2},
    {"q": "Разрешение экрана TempleOS?", "options": ["1920x1080", "800x600", "640x480", "1280x720"], "answer": 2},
    {"q": "Какой порт использует HTTP?", "options": ["21", "22", "80", "443"], "answer": 2},
    {"q": "Что такое Git?", "options": ["Язык программирования", "Система контроля версий", "База данных", "Веб-сервер"], "answer": 1},
    {"q": "Первый элемент массива в большинстве языков?", "options": ["1", "0", "-1", "Зависит"], "answer": 1},
    {"q": "Что такое API?", "options": ["Язык программирования", "База данных", "Интерфейс программирования", "Операционная система"], "answer": 2},
    {"q": "Скорость света в вакууме (прибл.)?", "options": ["200 000 км/с", "300 000 км/с", "400 000 км/с", "150 000 км/с"], "answer": 1},
    {"q": "Столица Японии?", "options": ["Осака", "Киото", "Токио", "Хиросима"], "answer": 2},
]

def make_board(board, game_id):
    symbols = {0: "⬜", 1: "❌", 2: "⭕"}
    keyboard = []
    for row in range(3):
        kb_row = []
        for col in range(3):
            idx = row * 3 + col
            kb_row.append(InlineKeyboardButton(symbols[board[idx]], callback_data=f"ttt_{game_id}_{idx}"))
        keyboard.append(kb_row)
    keyboard.append([InlineKeyboardButton("🏳️ Сдаться", callback_data=f"ttt_{game_id}_quit")])
    return InlineKeyboardMarkup(keyboard)

def check_winner(board):
    for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return board[combo[0]]
    return -1 if all(c != 0 for c in board) else 0

async def tictactoe_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = update.message.message_id
    board = [0] * 9
    context.bot_data[f"ttt_{game_id}"] = {
        "board": board, "current": 1,
        "players": {1: update.effective_user.id, 2: None},
        "player_names": {1: update.effective_user.full_name, 2: "???"},
    }
    await update.message.reply_text(
        terry_wrap(
            f"🎮 <b>DIVINE TICTACTOE INITIATED</b>\n\n"
            f"❌ {update.effective_user.full_name}\n⭕ Ожидает соперника...\n\nХод: ❌"
        ),
        reply_markup=make_board(board, game_id),
        parse_mode=ParseMode.HTML
    )

async def tictactoe_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    game_id = int(parts[1])
    game = context.bot_data.get(f"ttt_{game_id}")

    if not game:
        await query.edit_message_text("❌ ИГРА ИСТЕКЛА. GOD CLOSED IT.")
        return

    user = query.from_user

    if parts[2] == "quit":
        if user.id in game["players"].values():
            del context.bot_data[f"ttt_{game_id}"]
            await query.edit_message_text(terry_wrap(f"🏳️ {user.full_name} SURRENDERED. THE TEMPLE WITNESSED."), parse_mode=ParseMode.HTML)
        return

    cell = int(parts[2])

    if game["players"][2] is None and user.id != game["players"][1]:
        game["players"][2] = user.id
        game["player_names"][2] = user.full_name

    if user.id not in game["players"].values():
        await query.answer("Эта игра уже занята!", show_alert=True)
        return

    if user.id != game["players"][game["current"]]:
        sym = "❌" if game["current"] == 1 else "⭕"
        await query.answer(f"Сейчас ход {sym}!", show_alert=True)
        return

    if game["board"][cell] != 0:
        await query.answer("Клетка занята! GOD SEES YOUR CHEATING.", show_alert=True)
        return

    game["board"][cell] = game["current"]
    winner = check_winner(game["board"])

    if winner == -1:
        del context.bot_data[f"ttt_{game_id}"]
        await query.edit_message_text(
            terry_wrap(f"🤝 НИЧЬЯ. GOD IS AMBIVALENT.\n❌ {game['player_names'][1]} vs ⭕ {game['player_names'][2]}"),
            parse_mode=ParseMode.HTML
        )
        return

    if winner:
        sym = "❌" if winner == 1 else "⭕"
        name = game["player_names"][winner]
        del context.bot_data[f"ttt_{game_id}"]
        await query.edit_message_text(
            terry_wrap(f"🎉 {sym} <b>{name} WINS! GOD CHOSE THEM.</b>\n\n❌ {game['player_names'][1]} vs ⭕ {game['player_names'][2]}"),
            parse_mode=ParseMode.HTML
        )
        return

    game["current"] = 2 if game["current"] == 1 else 1
    sym = "❌" if game["current"] == 1 else "⭕"
    name = game["player_names"][game["current"]]

    await query.edit_message_text(
        terry_wrap(
            f"🎮 <b>DIVINE TICTACTOE</b>\n\n"
            f"❌ {game['player_names'][1]} vs ⭕ {game['player_names'][2]}\n\n"
            f"Ход: {sym} <b>{name}</b>"
        ),
        reply_markup=make_board(game["board"], game_id),
        parse_mode=ParseMode.HTML
    )

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(TRIVIA_QUESTIONS)
    game_id = update.message.message_id
    context.bot_data[f"quiz_{game_id}"] = {
        "answer": q["answer"], "question": q["q"], "answered": set()
    }
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{game_id}_{i}")] for i, opt in enumerate(q["options"])]
    await update.message.reply_text(
        terry_wrap(f"🧠 <b>DIVINE QUIZ:</b>\n\n❓ {q['q']}"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    parts = query.data.split("_")
    game_id = int(parts[1])
    chosen = int(parts[2])
    game = context.bot_data.get(f"quiz_{game_id}")

    if not game:
        await query.answer("Викторина завершена!", show_alert=True)
        return

    user = query.from_user
    if user.id in game["answered"]:
        await query.answer("Ты уже отвечал! THE TEMPLE KNOWS.", show_alert=True)
        return

    game["answered"].add(user.id)

    if chosen == game["answer"]:
        await query.answer(f"✅ ПРАВИЛЬНО! GOD BLESSES {user.first_name}!", show_alert=True)
        await query.edit_message_text(
            terry_wrap(f"🧠 <b>DIVINE QUIZ SOLVED!</b>\n\n{game['question']}\n\n✅ {user.mention_html()} ответил правильно! 🎉"),
            parse_mode=ParseMode.HTML
        )
        del context.bot_data[f"quiz_{game_id}"]
    else:
        await query.answer(f"❌ НЕПРАВИЛЬНО. THE TEMPLE LAUGHS.", show_alert=True)

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(TRIVIA_QUESTIONS)
    opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(q["options"]))
    correct = q["options"][q["answer"]]
    await update.message.reply_text(
        terry_wrap(f"🎯 <b>DIVINE TRIVIA:</b>\n\n{q['q']}\n\n{opts}\n\n||✅ Ответ: {correct}||"),
        parse_mode="MarkdownV2"
    )
