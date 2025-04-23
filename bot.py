from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- СЮЖЕТНЫЕ ДАННЫЕ И СОСТОЯНИЯ ---
intro_text = (
    "Ты просыпаешься в роскошной комнате дворца. Перед тобой — свиток.\n"
    "\n"
    "\u2022 Прочесть свиток (нажми /scroll)"
)

scroll_text = (
    "Свиток гласит: \"О великая Аполинариз, оставь страх — путь твой предначертан.\n"
    "Три испытания откроют тебе Истину. Первое ждет в зале зеркал.\"\n"
    "\n"
    "\u2022 Отправиться в зал зеркал (нажми /mirrors)"
)

mirrors_text = (
    "В зале зеркал появляется отражение, которое говорит загадку:\n\n"
    "'Нас двое, но ты видишь только одного. Мы отражаем свет и тайны.\n"
    "Если сложишь наш взгляд, откроется ключ.'\n\n"
    "\u2022 Что это? Введи свой ответ. (Подсказка: цифры, зеркала — это бинарный код)"
)

cipher_intro_text = (
    "Правильно! Зеркала отражают 0 и 1. Бинарный код — первая часть ключа.\n"
    "\n"
    "Теперь направляйся к библиотеке джинна. (/library)"
)

library_text = (
    "В библиотеке сидит старый джинн. Он говорит:\n\n"
    "'Всё, что написано, можно скрыть. И всё скрытое — можно раскрыть.\n"
    "Возьми этот свиток. Там тайна, но не для глаз, а для ума.'\n\n"
    "Ты видишь странный набор цифр: 01001000 01100101 01101100 01101100 01101111\n"
    "\n"
    "\u2022 Преобразуй их. (Подсказка: это бинарный код ASCII) — введи результат."
)

caesar_text = (
    "Ты разгадала! Это слово \"Hello\". Джинн кивает.\n"
    "\"Теперь, — говорит он, — применяй шифр, как древние воины — сдвиг на шесть вперёд.\"\n"
    "\n"
    "\u2022 Примени шифр Цезаря (+6) к слову 'Sheherazade'. Введи результат."
)

final_stage_text = (
    "Верно! Теперь ты знаешь: шифр Цезаря +6, бинарный код и текст объединены.\n"
    "\n"
    "Ты открываешь последний сундук. В нём — зашифрованное послание.\n"
    "Расшифруй его так: 1) переведи из двоичного в текст, 2) примени шифр Цезаря со сдвигом -6.\n"
    "\n"
    "\u2022 Вот сообщение: 01001000 01100101 01101100 01101100 01101111\n"
    "\u2022 Расшифруй и введи ответ."
)

end_text = (
    "Поздравляем! Ты прошла путь от тайн дворца до расшифровки древнего послания.\n"
    "Истина открыта тебе: \"Благословен тот, кто ищет смысл, а не золото.\"\n"
    "\n"
    "Конец. Хочешь сыграть снова? Нажми /start."
)

# --- СОСТОЯНИЯ ---
STATE = {}

# --- ХЭНДЛЕРЫ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE[update.effective_chat.id] = 'intro'
    await update.message.reply_text(intro_text)

async def scroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE[update.effective_chat.id] = 'mirrors'
    await update.message.reply_text(scroll_text)

async def mirrors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE[update.effective_chat.id] = 'mirror_riddle'
    await update.message.reply_text(mirrors_text)

async def library(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE[update.effective_chat.id] = 'library'
    await update.message.reply_text(library_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    state = STATE.get(user_id, '')
    text = update.message.text.strip().lower()

    if state == 'mirror_riddle':
        if text in ['0 и 1', '0 и 1.', 'бинарный код', 'бит', 'биты']:
            STATE[user_id] = 'cipher_intro'
            await update.message.reply_text(cipher_intro_text)
        else:
            await update.message.reply_text("Попробуй ещё раз. Это связано с зеркалами и числами.")

    elif state == 'library':
        if text == 'hello':
            STATE[user_id] = 'caesar'
            await update.message.reply_text(caesar_text)
        else:
            await update.message.reply_text("Неверно. Это обычное английское приветствие.")

    elif state == 'caesar':
        if text == 'ynknkxgzjfk':
            STATE[user_id] = 'final'
            await update.message.reply_text(final_stage_text)
        else:
            await update.message.reply_text("Неверно. Вспомни сдвиг на шесть букв вперёд.")

    elif state == 'final':
        if text == 'bzzrudiyzj':
            await update.message.reply_text(end_text)
            STATE[user_id] = 'end'
        else:
            await update.message.reply_text("Это не окончательный ответ. Попробуй снова.")

# --- MAIN ---
app = ApplicationBuilder().token("8169291502:AAHdi7rdUpl8cVNvl9zyUcMzdjpJLanVm5I").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scroll", scroll))
app.add_handler(CommandHandler("mirrors", mirrors))
app.add_handler(CommandHandler("library", library))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
