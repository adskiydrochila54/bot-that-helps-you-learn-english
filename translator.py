import telebot
from telebot import types
from deep_translator import GoogleTranslator

token = "7393728036:AAFIqmjyvn95fFF-6JH5AznmvqtQ7Dj97Ks"
bot = telebot.TeleBot(token)

user_languages = {}

def translate_text(text: str, target_language: str = "en") -> str:
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        return translator.translate(text)
    except Exception as e:
        return f"Translation error: {e}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_languages[message.chat.id] = "en"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Change Language")
    bot.send_message(message.chat.id,
        f"Hello, {message.from_user.first_name}!\n"
        f"Just send me any text, and I will translate it.\n\n"
        f"Default translation language: 🇬🇧 English.\n"
        f"Use /help for more info.",
        reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
        bot.send_message(message.chat.id,
                         "*How to use the Translator Bot:*\n\n"
                         "🔹 *Send any message* — and I will translate it to your selected language.\n"
                         "🔹 *Change language* — press the 🌐 *Change Language* button or use the command `/lang <code>`.\n\n"
                         "*Examples of language codes:*\n"
                         "`en` – English\n"
                         "`ru` – Russian\n"
                         "`es` – Spanish\n"
                         "`fr` – French\n"
                         "`de` – German\n\n"
                         "ℹ️ Default language is English.\n"
                         "💡 Try sending: `Привет! Как дела?`",
                         parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
        "*How to use the bot:*\n"
        "1. Send any text — I’ll translate it.\n"
        "2. Tap 'Change Language' or use /lang <language_code>.\n"
        "3. Examples:\n"
        "`en` — English\n`ru` — Russian\n`es` — Spanish\n`de` — German\n`fr` — French",
        parse_mode="Markdown")

@bot.message_handler(commands=['lang'])
def change_lang_command(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Usage example: /lang ru")
        return

    new_lang = parts[1].lower()
    try:
        GoogleTranslator(source='auto', target=new_lang)
        user_languages[message.chat.id] = new_lang
        bot.send_message(message.chat.id, f"Translation language set to: `{new_lang}`", parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, f"Invalid or unsupported language code: `{new_lang}`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Change Language")
def language_buttons(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    langs = [("🇬🇧 EN", "en"), ("🇷🇺 RU", "ru"), ("🇪🇸 ES", "es"), ("🇩🇪 DE", "de"), ("🇫🇷 FR", "fr")]
    buttons = [types.InlineKeyboardButton(text=name, callback_data=code) for name, code in langs]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Select a target language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_language_choice(call):
    lang = call.data
    try:
        GoogleTranslator(source='auto', target=lang)
        user_languages[call.message.chat.id] = lang
        bot.answer_callback_query(call.id, text=f"Language set to: {lang.upper()}")
        bot.send_message(call.message.chat.id, f"Now I will translate to `{lang}`.", parse_mode="Markdown")
    except:
        bot.answer_callback_query(call.id, text="Unsupported language.")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, "Please enter some text.")
        return

    lang = user_languages.get(message.chat.id, "en")
    translated = translate_text(text, lang)
    bot.send_message(message.chat.id, f"Translation:\n\n{translated}")

bot.infinity_polling()
