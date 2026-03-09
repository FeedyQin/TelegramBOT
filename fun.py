import random
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import mention, terry_wrap, terry_error
from config import BIBLE_VERSES

JOKES = [
    "— Почему программисты путают Halloween и Christmas?\n— Потому что Oct 31 == Dec 25!",
    "— Как называется боязнь Деда Мороза?\n— Клаустрофобия!",
    "— Что сказал ноль единице?\n— У тебя такой тонкий стан!",
    "— Почему скелеты не дерутся между собой?\n— У них нет смелости!",
    "Учитель: Иванов, из чего состоит вода?\n— Из Н, О и ещё двух других вещей.",
    "— Доктор, меня все игнорируют.\n— Следующий!",
    "— Папа, ты умеешь делать звуки животных?\n— Да. *молчит как рыба*",
    "Wi-Fi дома не работает. Пришлось поговорить с семьёй. Приятные люди!",
    "Диета — это искусство умирать с голоду, чтобы потом жить дольше.",
    "— Что общего у пивного завода и IT-компании?\n— Оба производят баги.",
    "— Вы верите в любовь с первого взгляда?\n— Нет, поэтому я смотрю по второму разу.",
    "Мозг: не забудь купить молоко.\nЯ в магазине: зачем я сюда пришёл?",
    "— Сколько программистов нужно, чтобы вкрутить лампочку?\n— Ни одного, это аппаратная проблема.",
    "— Почему Java-программисты носят очки?\n— Потому что они не видят sharp!",
    "Телефон разрядился. Пришлось самому думать о жизни. Ужасно.",
    "— В чём разница между пиццой и программистом?\n— Пицца может прокормить семью.",
    "— Как называется рыба без глаз?\n— Рыба! (fsh — fish без i)",
    "Оптимист: стакан наполовину полон.\nПессимист: наполовину пуст.\nПрограммист: стакан в два раза больше, чем нужно.",
    "— Дорогой, ты меня слушаешь?\n— Да, ты говоришь что-то про воскресенье.\n— Я говорю уже 20 минут про пятницу.",
    "Мой диет-план: если никто не видел как ты ел — калорий нет.",
    "— Почему коровы носят колокольчики?\n— Потому что рога не звенят!",
    "— Что такое умный блондин?\n— Золотой ретривер.",
    "Начальник: почему ты опоздал?\nЯ: вы же говорили не торопиться с работой.",
    "— Кто самый терпеливый человек в мире?\n— Тот, кто читает инструкции к IKEA.",
    "В детстве я думал, что взрослые всё знают. Теперь я взрослый. Это страшно.",
    "— Как программист открывает шампанское?\n— pop()!",
    "Я не ленивый. Я в режиме энергосбережения.",
    "— Что говорит кот когда его бьёт ток?\n— МЯЯЯУ (мяч = ток + мяу).",
    "Жена говорит: «Ты меня не слышишь». По крайней мере, я так думаю, что она говорит.",
    "— Почему математики боятся -273°C?\n— Это абсолютный ноль шансов!",
    "— Что общего у меня и вай-фая?\n— Оба сильны только дома.",
    "Мне не нужен будильник. Моя тревога справляется лучше.",
    "— Как называется медведь без ушей?\n— Медвь.",
    "— Почему нельзя верить атомам?\n— Они составляют всё!",
    "Кот опрокинул стакан воды. Я не злюсь. Я уважаю его хаотичную энергию.",
    "— Как называется испанец без машины?\n— Карлос.",
    "Программист умер и попал в ад. Там ему дали задачу: отсортировать бесконечный список. Он до сих пор доволен — хоть понятное ТЗ.",
    "— Почему Python лучше C++?\n— Потому что у Бога нет указателей.",
    "Я написал 'Hello World' в 15 лет. Потом 8 лет отлаживал.",
    "— Что говорит программист своей маме?\n— Мам, ты не понимаешь, это O(n log n), быстрее некуда!",
    "Мой код работает — я не знаю почему. Мой код не работает — я тоже не знаю почему.",
    "— Рекурсия — это...\n— см. Рекурсия.",
    "— Ты закончил задачу?\n— Почти. Осталось 5 минут.\n(Прошло 3 часа)\n— Почти. Осталось 5 минут.",
    "Git commit -m 'final'. Git commit -m 'final2'. Git commit -m 'ACTUAL_final'. Git commit -m 'please_work'.",
    "— Что такое full-stack разработчик?\n— Человек, который умеет плохо делать всё.",
    "Стек вызовов переполнен. Это не баг — это я описываю свои мысли.",
    "— Почему Линус Торвальдс злой?\n— Потому что у него Linux.",
    "— Как называется сон программиста?\n— Debugging in progress.",
    "Моя жизнь — это бесконечный while(true) без break.",
    "— Что сказал if-else на похоронах?\n— Иначе...",
    "— Как программист признаётся в любви?\n— if (you == perfect) { me.love(you); }",
    "— Сколько Git-коммитов нужно, чтобы написать резюме?\n— Не важно, главное что их 500+.",
    "Отладка — это как быть детективом в детективе, где ты и убийца, и жертва.",
    "— Как называется антивирус для людей?\n— Кофе.",
    "— В чём разница между разработчиком и пользователем?\n— Разработчик знает, кто виноват.",
    "Я не пью кофе. Я просто заряжаю батарейку нервной системы.",
    "— Почему темно в серверной?\n— Потому что там много облаков!",
    "— Что сказал HTML CSS?\n— Ты придаёшь мне смысл.",
    "— Почему JavaScript странный?\n— Потому что undefined == null, но undefined !== null.",
    "[] + [] = '' ... [] + {} = '[object Object]' ... {} + [] = 0. JAVASCRIPT IS GOD'S JOKE.",
    "— Что общего у кофе и мониторов?\n— Оба помогают видеть в темноте.",
    "— Как называется хакер в джунглях?\n— Jungle Script.",
    "— Почему Docker популярен?\n— Потому что «у меня работает» теперь официальный аргумент.",
    "Тест в продакшне — это смелость. Нет, это идиотизм. Нет, это смелость.",
    "— Что такое баг?\n— Незадокументированная фича.",
    "— Что такое фича?\n— Задокументированный баг.",
    "— Ты сделал бэкап?\n— Зачем?\n— ...\n— ...зачем?",
    "— Почему разработчики не смотрят в окно утром?\n— Тогда им нечем было бы заниматься после обеда.",
    "Agile — это когда ты не знаешь что делать, но делаешь это быстро.",
    "— Что такое senior developer?\n— Junior, который научился гуглить правильно.",
    "— Как объяснить рекурсию ребёнку?\n— Сначала объясни рекурсию.",
    "Я понял, что устал, когда начал комментировать код на русском, английском и матом одновременно.",
    "— Почему программист ушёл из ресторана?\n— Там не было меню типа JSON.",
    "— Как называется программист без кофе?\n— Баг.",
    "NULL — это не ничто. Это специальное ничто.",
    "— Как программист описывает выходные?\n— Undefined.",
    "— Что сказал массив стеку?\n— Ты мне не пара.",
    "— Зачем программисты носят тёмные очки?\n— Чтобы не видеть чужой код.",
    "— Что снится разработчику?\n— 0000 0000 0000 0000.",
    "— Как стать senior-разработчиком?\n— Скопировать с StackOverflow 10 000 раз.",
    "— Что сказал bool на свидании?\n— True или False — нет ничего между нами.",
    "Комментарий в коде: // TODO: это нужно исправить. Дата: 2017-03-14.",
    "— Почему программисты предпочитают тёмную тему?\n— Потому что светлое привлекает баги.",
    "— Как называется страх перед Git?\n— Merge-фобия.",
    "Иду в магазин. Жена говорит: купи хлеб, и если есть яйца — возьми десяток.\nЯ купил 10 хлебов. Были яйца.",
    "— Почему у программистов нет друзей?\n— Они deprecated всех ненужных.",
    "— Что значит «404» для студента?\n— Знания не найдены.",
    "— Как программист объясняет смерть?\n— Процесс завершён с кодом 0.",
    "Моё тело — это legacy-код. Работает, но никто не знает почему.",
    "— Как называется программист на пенсии?\n— Архитектор.",
    "— Сколько разработчиков нужно чтобы поменять лампочку?\n— Ни одного — это проблема DevOps.",
    "Я не баг. Я feature в стадии инкубации.",
    "— Что говорит программист когда видит баг в продакшне?\n— Работало вчера на локальной.",
    "— Почему хаскелисты счастливы?\n— Потому что у них нет side effects.",
    "— Как программисты едят суп?\n— Итеративно.",
    "— Что такое хороший код?\n— Код который понимает Бог. Хороший код — тот, что я написал вчера.",
    "— Почему переменные называют x, y, z?\n— Потому что a, b, c — для академиков, а temp — для трусов.",
    "Технический долг — это как кредит: всегда платишь больше чем брал.",
    "— Как называется программист, который не спит?\n— Backend-разработчик в пятницу вечером.",
    "— Сколько байт в мегабайте?\n— Зависит от того, кто спрашивает.",
    "— Почему компьютеры быстро считают?\n— Потому что цифры не возражают.",
]

EIGHTBALL_ANSWERS = [
    "✅ БЕССПОРНО. GOD SAID YES.",
    "✅ ПРЕДРЕШЕНО. THE TEMPLE CONFIRMS.",
    "✅ ДА, ОПРЕДЕЛЁННО. HOLY C SAYS SO.",
    "✅ МОЖЕШЬ БЫТЬ УВЕРЕН. KERNEL APPROVES.",
    "✅ МНЕ КАЖЕТСЯ ДА. DIVINE INTERRUPT: YES.",
    "🟡 НИКАКИХ СОМНЕНИЙ. RING 0 SAYS MAYBE.",
    "🟡 ВЕРОЯТНЕЕ ВСЕГО. THE SCROLLS SUGGEST YES.",
    "🟡 ХОРОШИЕ ПЕРСПЕКТИВЫ. GOD IS THINKING.",
    "🟡 ДА. SIMPLE OUTPUT FROM GOD.",
    "🟡 ЗНАКИ ГОВОРЯТ «ДА». DIVINE PATTERN MATCH.",
    "❓ ПОКА НЕЯСНО. GOD'S SCHEDULER IS BUSY.",
    "❓ СПРОСИ ПОЗЖЕ. DIVINE BUFFER OVERFLOW.",
    "❓ ЛУЧШЕ НЕ ЗНАТЬ. THE TEMPLE IS SILENT.",
    "❓ СЕЙЧАС НЕЛЬЗЯ ПРЕДСКАЗАТЬ. NULL RETURNED.",
    "❌ ДАЖЕ НЕ ДУМАЙ. GOD SAID ABSOLUTELY NOT.",
    "❌ МОЙ ОТВЕТ — НЕТ. THE KERNEL REJECTS.",
    "❌ ПО МОИМ ДАННЫМ — НЕТ. DIVINE COMPUTATION: FALSE.",
    "❌ ПЕРСПЕКТИВЫ НЕ ОЧЕНЬ. GOD SHAKES HIS HEAD.",
    "❌ ВЕСЬМА СОМНИТЕЛЬНО. THE TEMPLE FROWNS.",
    "🔥 ТОЛЬКО ЕСЛИ ТЫ НАПИШЕШЬ КОД НА HOLY C.",
]

QUOTES = [
    "«Единственный способ делать великую работу — любить то, что делаешь.» — Стив Джобс",
    "«Жизнь — это то, что с тобой происходит, пока ты строишь другие планы.» — Джон Леннон",
    "«Будь собой. Все остальные роли уже заняты.» — Оскар Уайльд",
    "«Ошибаться — человечно. Обвинять других — тоже очень человечно.» — Боб Хьюз",
    "«Умный человек решает проблему. Мудрый её обходит.» — Альберт Эйнштейн",
    "«Никогда не откладывай на завтра то, что можно сделать послезавтра.» — Марк Твен",
    "«Программы должны писаться для людей, а не для машин.» — Харольд Абельсон",
    "«Хороший код сам себя документирует.» — Роберт Мартин",
    "«TempleOS — это храм. Один пользователь. Один Бог. Один процессор.» — Терри Дэвис",
    "«Я самый талантливый программист, который когда-либо жил.» — Терри Дэвис",
    "«Бог использует случайные числа, чтобы говорить с нами.» — Терри Дэвис",
    "«Совершенство — враг хорошего, но друг великого.» — Вольтер",
    "«Знание — сила.» — Фрэнсис Бэкон",
    "«Я думаю, следовательно — я существую.» — Декарт",
    "«В конце концов всё встанет на своё место.» — Неизвестный автор",
    "«Не бойся медленно идти. Бойся стоять на месте.» — Китайская мудрость",
    "«Код — это поэзия.» — WordPress (и Бог)",
    "«Любой баг — это возможность узнать что-то новое о своей тупости.» — Каждый разработчик",
]

WOULD_YOU_RATHER = [
    ("летать", "быть невидимым"),
    ("знать все языки мира", "уметь говорить с животными"),
    ("никогда не спать", "спать 20 часов в сутки"),
    ("жить в прошлом", "жить в будущем"),
    ("быть богатым но несчастным", "бедным но счастливым"),
    ("читать мысли", "видеть будущее"),
    ("есть только сладкое", "есть только солёное"),
    ("никогда не мёрзнуть", "никогда не потеть"),
    ("выиграть лотерею", "найти настоящую любовь"),
    ("быть самым умным", "быть самым красивым"),
]

FACTS = [
    "🧠 Мозг человека использует 20% всей энергии тела, хотя весит лишь 2%.",
    "🐙 Осьминоги имеют три сердца и синюю кровь.",
    "🌍 Земля не является идеальной сферой — она немного сплюснута на полюсах.",
    "⚡ Молния горячее, чем поверхность Солнца — около 30 000°C.",
    "🐝 Пчела умирает после того, как ужалит, но только если жалит млекопитающих.",
    "🦈 Акулы старше деревьев. Они появились 450 млн лет назад.",
    "🍯 Мёд никогда не портится. В египетских гробницах нашли 3000-летний мёд.",
    "🐘 Слоны — единственные животные, которые не могут прыгать.",
    "🧊 Горячая вода замерзает быстрее холодной — эффект Мпембы.",
    "🌙 На Луне нет ветра, поэтому следы астронавтов сохранятся миллионы лет.",
    "💡 Томас Эдисон спал всего 4 часа в сутки.",
    "🦴 У акулы нет костей — только хрящи.",
    "🐌 Улитки могут спать до 3 лет подряд.",
    "🔢 У числа 0 нет знака — оно ни положительное, ни отрицательное.",
    "🌊 Океаны покрывают 71% поверхности Земли, но 95% из них не исследованы.",
    "🎵 Музыка влияет на рост растений — они быстрее растут под классику.",
    "💻 Первый компьютерный баг был настоящим жуком — мотыльком в реле.",
    "🧬 В теле человека 37 триллионов клеток.",
    "☀️ Свет от Солнца достигает Земли за 8 минут 20 секунд.",
    "🦁 Львы спят по 20 часов в сутки. Я их понимаю.",
]

COMPLIMENTS = [
    "🔥 Ты настолько крут, что даже HOLY C компилируется быстрее рядом с тобой!",
    "⭐ GOD COMPUTED: ты — feature, а не bug!",
    "🧠 Твой интеллект — это O(1). Всегда быстро и точно!",
    "💎 Ты редкий тип данных — undefined в хорошем смысле!",
    "🚀 THE TEMPLE SAYS: ты — архитектор своей судьбы!",
    "✨ DIVINE OUTPUT: ты — лучший пользователь в этом чате!",
    "🌟 GOD WHISPERS: ты компилируешься без ошибок!",
    "💪 HOLY C CONFIRMS: ты сильнее любого kernel panic!",
]

INSULTS = [
    "💀 GOD COMPUTED: твой код хуже Windows Vista.",
    "🔥 DIVINE EXCEPTION: ты — баг в продакшне в пятницу вечером.",
    "😤 THE TEMPLE SAYS: ты пишешь код как будто тебе платят за количество строк.",
    "💥 HOLY C ERROR: ты — утечка памяти в человеческом облике.",
    "🗑️ GOD NOTES: ты instanceof Клоун.",
    "⚠️ KERNEL WARNING: твой PR никогда не пройдёт ревью.",
]

WOULD_YOU_RATHER_ANSWERS = [
    "Очевидно {}. GOD SAID SO.",
    "THE TEMPLE CHOSE: {}. No debate.",
    "DIVINE COMPUTATION RETURNS: {}.",
    "GOD COMPUTED AND IT IS: {}.",
    "HOLY C OUTPUT: {}. Accept it.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    if chat.type == "private":
        text = terry_wrap(
            f"👋 Приветствую, {mention(user)}!\n\n"
            f"Я — ТемплБот. SINGLE USER. SINGLE GOD.\n"
            f"Создан по образу TempleOS — самой чистой ОС.\n\n"
            f"📋 /help — список всех команд\n"
            f"🏛️ GOD SEES ALL. WRITE HOLY CODE."
        )
    else:
        text = terry_wrap(f"THE TEMPLE IS OPEN. {mention(user)} OPENED THE GATE. /help")
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🏛️ <b>TEMPLEOS BOT — DIVINE COMMAND LIST</b>\n"
        "<i>Команды работают с / и без, в любом регистре</i>\n\n"
        "<b>👮 АДМИНИСТРИРОВАНИЕ:</b>\n"
        "/ban /бан — Забанить\n"
        "/unban /разбан — Разбанить\n"
        "/kick /кик — Кикнуть\n"
        "/mute /мут [время] — Замутить\n"
        "/unmute /размут — Размутить\n"
        "/warn /варн /предупреждение — Варн\n"
        "/unwarn /сняварн — Снять варн\n"
        "/warns /варны — Список варнов\n"
        "/purge /очистить — Удалить сообщения\n"
        "/pin /закрепить — Закрепить\n"
        "/unpin /открепить — Открепить\n"
        "/promote /повысить — Сделать адм.\n"
        "/demote /понизить — Снять адм.\n"
        "/admins /админы — Список адм.\n\n"
        "<b>📝 ЗАМЕТКИ:</b>\n"
        "/note /заметка [имя] [текст] — Сохранить\n"
        "/notes /заметки — Все заметки\n"
        "/get /покажи [имя] — Показать заметку\n"
        "/delnote /удзаметку [имя] — Удалить\n\n"
        "<b>🎮 ИГРЫ:</b>\n"
        "/ttt /крестики — Крестики-нолики\n"
        "/quiz /викторина — Викторина\n"
        "/trivia /вопрос — Вопрос-ответ\n"
        "/truth /правда — Правда или действие\n"
        "/dare /действие — Действие\n\n"
        "<b>🎉 РАЗВЛЕЧЕНИЯ:</b>\n"
        "/8ball /шар [вопрос] — Магический шар\n"
        "/roll /кубик [число] — Бросить кубик\n"
        "/flip /монетка — Орёл/Решка\n"
        "/joke /анекдот /шутка — Анекдот\n"
        "/quote /цитата — Цитата\n"
        "/ship /совместимость — Шип\n"
        "/rate /оценить — Оценка\n"
        "/choose /выбор /выбери — Выбор\n"
        "/calc /калькулятор — Калькулятор\n"
        "/wyr /или — Что предпочесть\n"
        "/fact /факт — Интересный факт\n"
        "/compliment /комплимент — Комплимент\n"
        "/insult /оскорбление — Оскорбление\n"
        "/bible /библия — Стих из Библии\n"
        "/horoscope /гороскоп — Гороскоп\n"
        "/password /пароль — Пароль\n"
        "/rps /ксо — Камень-ножницы-бумага\n"
        "/slot /слот — Слот-машина\n"
        "/dice /кости — Бросить кости\n"
        "/fortune /судьба — Предсказание\n"
        "/ascii /аски — ASCII-арт\n\n"
        "<b>ℹ️ ИНФОРМАЦИЯ:</b>\n"
        "/id /айди — ID\n"
        "/info /инфо — Инфо о пользователе\n"
        "/ping /пинг — Пинг\n"
        "/stats /стата — Статистика\n"
        "/chatinfo /инфочата — Инфо о чате\n"
        "/time /время — Текущее время\n\n"
        "<b>🐱 МЕДИА:</b>\n"
        "/cat /кот — Фото котика\n"
        "/dog /собака — Фото собаки\n"
        "/meme /мем — Мем\n\n"
        "<i>GOD HATES BLOAT. BUT GOD LOVES FEATURES.</i>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user
    chat = update.effective_chat
    try:
        member = await chat.get_member(user.id)
        status_map = {
            "creator": "👑 Владелец",
            "administrator": "⭐ Администратор",
            "member": "👤 Участник",
            "restricted": "🔇 Ограничен",
            "left": "🚪 Покинул",
            "kicked": "🔨 Забанен"
        }
        status = status_map.get(member.status, member.status)
    except Exception:
        status = "❓ UNDEFINED"
    text = terry_wrap(
        f"👤 <b>DIVINE USER RECORD:</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'нет'}\n"
        f"🤖 Бот: {'Да' if user.is_bot else 'Нет'}\n"
        f"🌐 Язык: {user.language_code or 'UNKNOWN'}\n"
        f"📊 Статус: {status}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await update.message.reply_text(
            terry_wrap(f"🆔 ID {mention(target)}: <code>{target.id}</code>"),
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            terry_wrap(f"🆔 ВАШ ID: <code>{user.id}</code>\n💬 ID ЧАТА: <code>{chat.id}</code>"),
            parse_mode=ParseMode.HTML
        )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import time
    start = time.time()
    msg = await update.message.reply_text("🏓 DIVINE PING IN PROGRESS...")
    end = time.time()
    ms = round((end - start) * 1000)
    await msg.edit_text(
        terry_wrap(f"🏓 PONG!\n⚡ Задержка: <code>{ms}ms</code>\n{'GOD IS FAST.' if ms < 100 else 'NETWORK BLOAT DETECTED.'}"),
        parse_mode=ParseMode.HTML
    )

async def chatinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        count = await chat.get_member_count()
    except Exception:
        count = "?"
    text = terry_wrap(
        f"💬 <b>CHAT DIVINE RECORD:</b>\n\n"
        f"🆔 ID: <code>{chat.id}</code>\n"
        f"📛 Название: {chat.title}\n"
        f"👥 Участников: {count}\n"
        f"🔗 Username: @{chat.username or 'нет'}\n"
        f"📝 Тип: {chat.type}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user
    from data.database import get_stats
    s = get_stats(update.effective_chat.id, user.id)
    await update.message.reply_text(
        terry_wrap(
            f"📊 <b>DIVINE STATS: {mention(user)}</b>\n\n"
            f"💬 Сообщений: {s.get('messages', 0)}\n"
            f"⌨️ Команд: {s.get('commands', 0)}\n"
            f"📅 В чате с: {s.get('joined', 'UNKNOWN')[:10] if s.get('joined') else 'UNKNOWN'}"
        ),
        parse_mode=ParseMode.HTML
    )

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    now = datetime.now()
    await update.message.reply_text(
        terry_wrap(
            f"🕐 <b>DIVINE TIME:</b>\n\n"
            f"📅 Дата: {now.strftime('%d.%m.%Y')}\n"
            f"🕒 Время (UTC+3): {now.strftime('%H:%M:%S')}\n"
            f"📆 День недели: {['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'][now.weekday()]}\n"
            f"📊 День года: {now.timetuple().tm_yday}/365"
        ),
        parse_mode=ParseMode.HTML
    )

async def eightball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            terry_wrap("❓ ЗАДАЙ ВОПРОС!\nПример: /8ball Буду ли я богатым?"),
            parse_mode=ParseMode.HTML
        )
        return
    question = " ".join(context.args)
    answer = random.choice(EIGHTBALL_ANSWERS)
    await update.message.reply_text(
        terry_wrap(f"🎱 <b>ВОПРОС:</b> {question}\n\n<b>ОТВЕТ:</b> {answer}"),
        parse_mode=ParseMode.HTML
    )

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sides = 6
    if context.args:
        try:
            sides = max(2, int(context.args[0]))
        except ValueError:
            pass
    result = random.randint(1, sides)
    bar = "█" * int((result / sides) * 10) + "░" * (10 - int((result / sides) * 10))
    await update.message.reply_text(
        terry_wrap(f"🎲 КУБИК d{sides}\n\n[{bar}]\n\n<b>РЕЗУЛЬТАТ: {result}</b>"),
        parse_mode=ParseMode.HTML
    )

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.choice([("🦅 ОРЁЛ", "GOD'S FACE"), ("🏛 РЕШКА", "THE TEMPLE SIDE")])
    await update.message.reply_text(
        terry_wrap(f"🪙 МОНЕТКА БРОШЕНА...\n\n<b>{result[0]}</b>\n{result[1]}"),
        parse_mode=ParseMode.HTML
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    j = random.choice(JOKES)
    await update.message.reply_text(
        terry_wrap(f"😂 <b>DIVINE JOKE:</b>\n\n{j}"),
        parse_mode=ParseMode.HTML
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUOTES)
    await update.message.reply_text(
        terry_wrap(f"💭 <b>DIVINE QUOTE:</b>\n\n{q}"),
        parse_mode=ParseMode.HTML
    )

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(terry_wrap("❓ ЧТО ОЦЕНИТЬ?\nПример: /rate моя жизнь"), parse_mode=ParseMode.HTML)
        return
    thing = " ".join(context.args)
    score = random.randint(0, 100)
    emojis = ["💀", "😔", "😔", "😐", "😐", "😐", "😊", "😊", "🔥", "🔥", "🔱"]
    emoji = emojis[score // 10]
    bar = "█" * (score // 10) + "░" * (10 - score // 10)
    await update.message.reply_text(
        terry_wrap(f"{emoji} <b>GOD RATES: {thing}</b>\n\n[{bar}] {score}/100"),
        parse_mode=ParseMode.HTML
    )

async def ship(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user1 = update.effective_user
        user2 = update.message.reply_to_message.from_user
        name1 = mention(user1)
        name2 = mention(user2)
    elif len(context.args) >= 2:
        sep = "|" if "|" in " ".join(context.args) else None
        if sep:
            parts = " ".join(context.args).split("|")
            name1, name2 = parts[0].strip(), parts[1].strip()
        else:
            name1 = context.args[0]
            name2 = " ".join(context.args[1:])
    else:
        await update.message.reply_text(terry_wrap("❓ ОТВЕТЬ НА СООБЩЕНИЕ или /ship Иван | Мария"), parse_mode=ParseMode.HTML)
        return
    score = random.randint(0, 100)
    hearts = "❤️" * (score // 20) + "🖤" * (5 - score // 20)
    verdict = "💍 ИДЕАЛЬНАЯ ПАРА. GOD BLESSES THIS UNION." if score > 80 else "💔 НЕ СУДЬБА. THE TEMPLE REJECTS." if score < 30 else "💝 ЕСТЬ ШАНСЫ. HOLY C SAYS MAYBE."
    await update.message.reply_text(
        terry_wrap(f"💕 <b>DIVINE COMPATIBILITY:</b>\n\n{name1} + {name2}\n{hearts} {score}%\n\n{verdict}"),
        parse_mode=ParseMode.HTML
    )

async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(terry_wrap("❓ /choose пицца | суши | бургер"), parse_mode=ParseMode.HTML)
        return
    text = " ".join(context.args)
    options = [o.strip() for o in text.replace(",", "|").split("|") if o.strip()]
    if len(options) < 2:
        await update.message.reply_text(terry_wrap("❓ НУЖНО МИНИМУМ 2 ВАРИАНТА. Через | или запятую."), parse_mode=ParseMode.HTML)
        return
    choice = random.choice(options)
    losers = [o for o in options if o != choice]
    await update.message.reply_text(
        terry_wrap(f"🎯 <b>GOD CHOSE:</b> {choice}\n\n❌ Отвергнуто: {', '.join(losers)}"),
        parse_mode=ParseMode.HTML
    )

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(terry_wrap("❓ /calc 2 + 2 * 10"), parse_mode=ParseMode.HTML)
        return
    expr = " ".join(context.args)
    if not all(c in "0123456789+-*/()., %**" for c in expr.replace("**", "")):
        await update.message.reply_text(terry_wrap("❌ DIVINE EXCEPTION: Недопустимые символы!"), parse_mode=ParseMode.HTML)
        return
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        await update.message.reply_text(
            terry_wrap(f"🧮 <code>{expr}</code> = <b>{result}</b>"),
            parse_mode=ParseMode.HTML
        )
    except Exception:
        await update.message.reply_text(terry_wrap("❌ KERNEL PANIC: Ошибка в выражении!"), parse_mode=ParseMode.HTML)

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        terry_wrap(f"🧠 <b>DIVINE FACT:</b>\n\n{random.choice(FACTS)}"),
        parse_mode=ParseMode.HTML
    )

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        target = mention(user)
    else:
        target = mention(update.effective_user)
    await update.message.reply_text(
        terry_wrap(f"{random.choice(COMPLIMENTS)}\n\n👑 {target}"),
        parse_mode=ParseMode.HTML
    )

async def insult(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        target = mention(user)
    else:
        target = mention(update.effective_user)
    await update.message.reply_text(
        terry_wrap(f"{random.choice(INSULTS)}\n\n💀 {target}"),
        parse_mode=ParseMode.HTML
    )

async def bible(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        terry_wrap(f"📖 <b>THE WORD OF GOD:</b>\n\n<i>{random.choice(BIBLE_VERSES)}</i>"),
        parse_mode=ParseMode.HTML
    )

async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    forecasts = [
        "Сегодня Бог думает о тебе. Напиши код на Holy C.",
        "Звёзды сказали: пей воду и закрой 47 вкладок.",
        "Великие дела ждут тебя. Или просто хороший обед.",
        "GOD COMPUTED: твой день будет лучше чем вчера.",
        "Сегодня тебя ждёт неожиданное. Может баг. Может удача.",
        "Звёзды молчат. Это хорошо — у Бога нет segfault.",
        "Кто-то думает о тебе. Это либо Бог, либо баг в продакшне.",
        "THE TEMPLE PREDICTS: выключи компьютер и поспи.",
        "Сегодня хороший день для рефакторинга жизни.",
        "Юпитер в созвездии Компилятора — жди merge conflict.",
    ]
    sign = random.choice(signs) if not context.args else " ".join(context.args)
    await update.message.reply_text(
        terry_wrap(f"⭐ <b>DIVINE HOROSCOPE: {sign}</b>\n\n{random.choice(forecasts)}"),
        parse_mode=ParseMode.HTML
    )

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import string
    length = 16
    if context.args:
        try:
            length = max(8, min(64, int(context.args[0])))
        except ValueError:
            pass
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choices(chars, k=length))
    await update.message.reply_text(
        terry_wrap(f"🔐 <b>DIVINE PASSWORD ({length} символов):</b>\n\n<code>{pwd}</code>\n\n<i>NEVER SHARE. GOD SEES IT.</i>"),
        parse_mode=ParseMode.HTML
    )

async def rps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choices = {"камень": "🪨", "ножницы": "✂️", "бумага": "📄"}
    bot_choice_key = random.choice(list(choices.keys()))
    bot_choice = choices[bot_choice_key]

    user_arg = " ".join(context.args).lower().strip() if context.args else ""
    user_choice_key = None
    for key in choices:
        if key in user_arg or user_arg in key[:3]:
            user_choice_key = key
            break

    if not user_choice_key:
        keyboard_text = (
            f"🎮 <b>DIVINE RPS — выбери:</b>\n\n"
            f"/rps камень 🪨\n/rps ножницы ✂️\n/rps бумага 📄"
        )
        await update.message.reply_text(terry_wrap(keyboard_text), parse_mode=ParseMode.HTML)
        return

    user_icon = choices[user_choice_key]
    wins = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}

    if user_choice_key == bot_choice_key:
        result = "🤝 НИЧЬЯ. GOD IS INDIFFERENT."
    elif wins[user_choice_key] == bot_choice_key:
        result = "🎉 ТЫ ПОБЕДИЛ! GOD ALLOWED THIS."
    else:
        result = "💀 ТЫ ПРОИГРАЛ. THE TEMPLE WINS."

    await update.message.reply_text(
        terry_wrap(f"Ты: {user_icon} {user_choice_key}\nБот: {bot_choice} {bot_choice_key}\n\n{result}"),
        parse_mode=ParseMode.HTML
    )

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbols = ["🍒", "🍋", "🍊", "🍇", "⭐", "💎", "7️⃣", "🔔", "🏛️"]
    weights = [30, 25, 20, 15, 5, 3, 1, 1, 0.1]
    reels = random.choices(symbols, weights=weights, k=3)
    line = " | ".join(reels)

    if len(set(reels)) == 1:
        if reels[0] == "🏛️":
            result = "🔱 DIVINE JACKPOT!! GOD HIMSELF BLESSED YOU!!"
        elif reels[0] == "7️⃣":
            result = "💰 ДЖЕКПОТ! THE TEMPLE PAYS OUT!"
        elif reels[0] == "💎":
            result = "💎 БРИЛЛИАНТОВЫЙ ВЫИГРЫШ! HOLY C COMPUTED THIS!"
        else:
            result = "🎉 ВЫИГРЫШ! GOD SMILES UPON YOU!"
    elif len(set(reels)) == 2:
        result = "🟡 ПОЧТИ... GOD IS TEASING YOU."
    else:
        result = "❌ НЕ ПОВЕЗЛО. THE KERNEL REJECTS YOUR COINS."

    await update.message.reply_text(
        terry_wrap(f"🎰 <b>DIVINE SLOT MACHINE:</b>\n\n[ {line} ]\n\n{result}"),
        parse_mode=ParseMode.HTML
    )

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = 2
    sides = 6
    if context.args:
        try:
            if "d" in context.args[0].lower():
                parts = context.args[0].lower().split("d")
                count = min(10, int(parts[0]) if parts[0] else 2)
                sides = min(100, int(parts[1]))
            else:
                count = min(10, int(context.args[0]))
        except Exception:
            pass
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    rolls_str = " + ".join(str(r) for r in rolls)
    await update.message.reply_text(
        terry_wrap(f"🎲 <b>DIVINE DICE ({count}d{sides}):</b>\n\n{rolls_str} = <b>{total}</b>"),
        parse_mode=ParseMode.HTML
    )

async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fortunes = [
        "Скоро тебя ждёт приятный сюрприз. GOD ARRANGED IT.",
        "Твой следующий код будет компилироваться с первого раза. MIRACLE DETECTED.",
        "Осторожно с понедельником. THE KERNEL IS UNSTABLE.",
        "Бог видит твои старания. THE TEMPLE APPROVES.",
        "Сегодня хороший день для новых начинаний. DIVINE INTERRUPT: BEGIN.",
        "Чья-то мысль о тебе прямо сейчас. GOD BROADCAST THIS.",
        "Удача в твоих руках. LITERALLY. YOUR HANDS TYPE THE CODE.",
        "Не бойся ошибок. Даже TempleOS имел баги. GOD FIXED THEM.",
        "Твоя звезда восходит. ORBITAL CALCULATION CONFIRMED.",
        "Хорошие новости идут к тебе. DIVINE PACKET INCOMING.",
        "Твой следующий PR примут без правок. IMPOSSIBLE BUT GOD WILLS IT.",
        "Остерегайся deprecated-людей в своей жизни.",
        "В ближайшее время тебя ждёт merge без конфликтов. AMEN.",
    ]
    await update.message.reply_text(
        terry_wrap(f"🔮 <b>DIVINE FORTUNE:</b>\n\n<i>{random.choice(fortunes)}</i>"),
        parse_mode=ParseMode.HTML
    )

async def wyr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and "|" in " ".join(context.args):
        parts = " ".join(context.args).split("|")
        if len(parts) >= 2:
            opt1, opt2 = parts[0].strip(), parts[1].strip()
        else:
            opt1, opt2 = random.choice(WOULD_YOU_RATHER)
    else:
        opt1, opt2 = random.choice(WOULD_YOU_RATHER)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(f"1️⃣ {opt1}", callback_data=f"wyr_1_{opt1[:30]}"),
        InlineKeyboardButton(f"2️⃣ {opt2}", callback_data=f"wyr_2_{opt2[:30]}")
    ]])
    await update.message.reply_text(
        terry_wrap(f"🤔 <b>DIVINE DILEMMA:</b>\n\n<b>1️⃣ {opt1}</b>\n\nили\n\n<b>2️⃣ {opt2}</b>"),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

async def wyr_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_", 2)
    choice_num = parts[1]
    choice_text = parts[2]
    answers = [
        f"Очевидно {choice_text}. GOD SAID SO.",
        f"THE TEMPLE CHOSE: {choice_text}.",
        f"DIVINE COMPUTATION: {choice_text}.",
        f"GOD NODS AT: {choice_text}.",
    ]
    await query.answer(random.choice(answers), show_alert=True)

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    truths = [
        "Что ты скрываешь от своих друзей?",
        "Назови своё самое большое сожаление.",
        "Кто твоя тайная симпатия в этом чате?",
        "Какой твой самый стыдный момент?",
        "Что ты никогда не признаешь вслух?",
        "Когда ты последний раз плакал?",
        "Что тебя бесит больше всего в людях?",
        "Какой твой самый большой страх?",
        "Кем ты хотел стать в детстве?",
        "Какую ложь ты рассказывал чаще всего?",
        "Что ты делал втайне, о чём сейчас не жалеешь?",
        "Назови троих людей в чате которым доверяешь.",
    ]
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    await update.message.reply_text(
        terry_wrap(f"😇 <b>DIVINE TRUTH для {mention(user)}:</b>\n\n❓ {random.choice(truths)}"),
        parse_mode=ParseMode.HTML
    )

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dares = [
        "Напиши 'GOD IS REAL' в следующих 3 сообщениях.",
        "Отправь голосовое сообщение и скажи что думаешь о TempleOS.",
        "Поставь реакцию ❤️ на последние 5 сообщений.",
        "Напиши своё мнение о Holy C честно.",
        "Признайся в чём-нибудь стыдном прямо сейчас.",
        "Напиши комплимент каждому человеку в чате.",
        "Отправь своё фото с рукой на голове.",
        "Напиши текст песни которую слушаешь прямо сейчас.",
        "Скажи что-нибудь на языке который не знаешь.",
        "Напиши хайку про программирование.",
        "Поспорь сам с собой в следующих 3 сообщениях.",
    ]
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    await update.message.reply_text(
        terry_wrap(f"😈 <b>DIVINE DARE для {mention(user)}:</b>\n\n⚡ {random.choice(dares)}"),
        parse_mode=ParseMode.HTML
    )

async def ascii_art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arts = [
        "```\n  /\\_/\\  \n( o.o ) \n > ^ <\n```",
        "```\n    ___\n   (o o)\n  (  V  )\n /--m-m-\n```",
        "```\n⠀⠀⢀⣴⣦⡀\n⠀⢀⣿⣿⣿⣷\n⠀⢸⣿⣿⣿⣿\n⠀⠈⠛⠛⠛⠁\n```",
        "```\n  _____\n |     |\n | GOD |\n |_____|\n   | |\n  _| |_\n```",
        "```\n .-''-.\n|  o o  |\n|  ___  |\n '-----'\nTEMPLEOS\n```",
    ]
    word = " ".join(context.args) if context.args else None
    if word:
        letters = {
            "A": "/-\\|=|", "B": "|-\\|_/", "C": "/--\\--/", "E": "|=_|=", "G": "/--.|-G",
            "H": "| || |", "I": "=I=", "L": "|  |__", "O": "/--\\|  |\\--/",
            "S": "/--._/--/", "T": "=T=T=",
        }
        await update.message.reply_text(
            terry_wrap(f"🔤 <b>DIVINE ASCII ART:</b>\n\n{random.choice(arts)}"),
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            terry_wrap(f"🎨 <b>DIVINE ASCII ART:</b>\n\n{random.choice(arts)}"),
            parse_mode=ParseMode.HTML
        )

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                await update.message.reply_photo(data[0]["url"], caption="🐱 DIVINE CAT. GOD MADE THIS CREATURE.")
    except Exception:
        await update.message.reply_text(terry_wrap("😿 API КОТОВ УПАЛ. ДАЖЕ БОГ НЕ МОЖЕТ ПОМОЧЬ."), parse_mode=ParseMode.HTML)

async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                await update.message.reply_photo(data["message"], caption="🐶 DIVINE DOG. GOD'S LOYAL CREATURE.")
    except Exception:
        await update.message.reply_text(terry_wrap("🐾 API СОБАК УПАЛ. KERNEL PANIC."), parse_mode=ParseMode.HTML)

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                await update.message.reply_photo(
                    data["url"],
                    caption=f"😂 DIVINE MEME: {data.get('title', 'GOD APPROVED')}"
                )
    except Exception:
        await update.message.reply_text(terry_wrap("😅 МЕМ-АПИ УПАЛ. DIVINE EXCEPTION."), parse_mode=ParseMode.HTML)

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data.database import set_note
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(terry_wrap("❓ /note имя текст"), parse_mode=ParseMode.HTML)
        return
    name = context.args[0]
    text = " ".join(context.args[1:])
    set_note(update.effective_chat.id, name, text)
    await update.message.reply_text(terry_wrap(f"📝 ЗАМЕТКА '<b>{name}</b>' СОХРАНЕНА. GOD REMEMBERS."), parse_mode=ParseMode.HTML)

async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data.database import get_notes
    all_notes = get_notes(update.effective_chat.id)
    if not all_notes:
        await update.message.reply_text(terry_wrap("📭 ЗАМЕТОК НЕТ. EMPTY AS THE VOID."), parse_mode=ParseMode.HTML)
        return
    text = "📝 <b>DIVINE NOTES:</b>\n\n" + "\n".join(f"• <code>{k}</code>" for k in all_notes.keys())
    await update.message.reply_text(terry_wrap(text), parse_mode=ParseMode.HTML)

async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data.database import get_notes
    if not context.args:
        await update.message.reply_text(terry_wrap("❓ /get имя"), parse_mode=ParseMode.HTML)
        return
    name = context.args[0].lower()
    all_notes = get_notes(update.effective_chat.id)
    if name not in all_notes:
        await update.message.reply_text(terry_wrap(f"❌ ЗАМЕТКА '{name}' НЕ НАЙДЕНА. VOID RETURNED."), parse_mode=ParseMode.HTML)
        return
    await update.message.reply_text(terry_wrap(f"📝 <b>{name}:</b>\n\n{all_notes[name]}"), parse_mode=ParseMode.HTML)

async def del_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data.database import del_note
    if not context.args:
        await update.message.reply_text(terry_wrap("❓ /delnote имя"), parse_mode=ParseMode.HTML)
        return
    name = context.args[0]
    if del_note(update.effective_chat.id, name):
        await update.message.reply_text(terry_wrap(f"🗑️ ЗАМЕТКА '<b>{name}</b>' УДАЛЕНА. MEMORY FREED."), parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(terry_wrap(f"❌ ЗАМЕТКА '{name}' НЕ НАЙДЕНА."), parse_mode=ParseMode.HTML)
