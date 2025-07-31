import random
import telebot
from telebot import types

words ={ "A1": [
    {"word": "book", "translate": "книга", "example": "This book is interesting."},
    {"word": "apple", "translate": "яблоко", "example": "I eat an apple."},
    {"word": "dog", "translate": "собака", "example": "The dog is friendly."},
    {"word": "water", "translate": "вода", "example": "Can I have some water?"},
    {"word": "school", "translate": "школа", "example": "She goes to school every day."},
    {"word": "table", "translate": "стол", "example": "The keys are on the table."},
    {"word": "car", "translate": "машина", "example": "My car is blue."},
    {"word": "chair", "translate": "стул", "example": "He sat on the chair."}
],

    "A2": [
        {"word": "confused", "translate": "смущённый", "example": "He looked confused."},
        {"word": "afraid", "translate": "испуганный", "example": "I am afraid of heights."},
        {"word": "travel", "translate": "путешествовать", "example": "We love to travel in summer."},
        {"word": "borrow", "translate": "одолжить", "example": "Can I borrow your pen?"},
        {"word": "angry", "translate": "злой", "example": "She was angry about the delay."},
        {"word": "tired", "translate": "уставший", "example": "I feel tired after work."},
        {"word": "hungry", "translate": "голодный", "example": "They were very hungry."},
        {"word": "expensive", "translate": "дорогой", "example": "That phone is too expensive."}
    ]

}

user_levels = {}
user_answers = {}

token = '8163723730:AAHBC8jPjga8G0rLv2SKCaMu1-UhybFBNh0'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("A1", "A2")
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}! Choose your English level:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["A1", "A2"])
def set_level(message):
    user_levels[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Level {message.text} selected. Use /word or /quiz to start learning!")

@bot.message_handler(commands=['word'])
def send_word(message):
    level = user_levels.get(message.chat.id, "A1")
    word_data = random.choice(words[level])
    text = f'{word_data["word"]} – {word_data["translate"]}\n_{word_data["example"]}_'
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    level = user_levels.get(message.chat.id, "A1")
    question = random.choice(words[level])
    correct_answer = question["translate"]


    other_words = [w["translate"] for w in words[level] if w["translate"] != correct_answer]
    wrong_answers = random.sample(other_words, min(3, len(other_words)))

    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    user_answers[message.chat.id] = correct_answer

    markup = types.InlineKeyboardMarkup()
    for option in options:
        button = types.InlineKeyboardButton(text=option, callback_data=option)
        markup.add(button)

    bot.send_message(message.chat.id, f"What is the translation of: *{question['word']}*?",
                     reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def check_answer(call):
    correct = user_answers.get(call.message.chat.id)
    chosen = call.data

    if chosen == correct:
        bot.answer_callback_query(call.id, "Correct!")
        bot.send_message(call.message.chat.id, "Well done!")
    else:
        bot.answer_callback_query(call.id, "Wrong!")
        bot.send_message(call.message.chat.id, f"Correct answer was: *{correct}*", parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Use /word or /quiz to start learning!, "
                                      f"/start to choose level, /help for this menu")

@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def unknown_command(message):
    bot.send_message(message.chat.id, "Извините, я не знаю такую команду. Попробуйте /help.")


bot.infinity_polling()
