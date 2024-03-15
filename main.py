from freeGPT import Client
import telebot
from telebot import types
from googletrans import Translator
from io import BytesIO


bot = telebot.TeleBot('5929520133:AAGpq-gt6I40hlEWx7JgW5qUz4-st3MOTds')


# Start Helop
@bot.message_handler(commands=['start','help'])
def start_help_comands(message):
    text_start = '''Привет этот бот умеет генерить фото и в нём есть ChatGPT'''

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    chat_gpt = types.KeyboardButton("ChatGPT")
    image = types.KeyboardButton("Сгенерить фото")
    markup.add(chat_gpt, image)
    bot.send_message(message.chat.id, text_start, reply_markup=markup)


# text
@bot.message_handler(content_types=['text'])
def Chat_GPT(message):
    if message.text == 'Сгенерить фото':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        raspisan_call = types.KeyboardButton("выход")
        markup.add(raspisan_call)
        bot.send_message(message.chat.id, "Пожалуйсто отправте описание фото:", reply_markup=markup)

        bot.register_next_step_handler(message, handle_image_message)


    if message.text == 'ChatGPT':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        raspisan_call = types.KeyboardButton("выход")
        markup.add(raspisan_call)
        bot.send_message(message.chat.id, "Пожалуйсто отправте сообщение:", reply_markup=markup)

        bot.register_next_step_handler(message, handle_user_message)

    else:
        bot.send_message(message.chat.id, "Я вас не понимаю напишите /help")

def handle_user_message(message):
    if message.text == "выход":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        chat_gpt = types.KeyboardButton("ChatGPT")
        image = types.KeyboardButton("Сгенерить фото")
        markup.add(chat_gpt, image)
        bot.send_message(message.chat.id, "Выход", reply_markup=markup)

    else:
        bot.register_next_step_handler(message, handle_user_message)

        bot.send_chat_action(message.chat.id, 'typing')
        resp = Client.create_completion("gpt3", message.text)
        translator = Translator()
        translation = translator.translate(resp, src='en', dest='ru')

        bot.send_message(message.chat.id, translation.text)


def  handle_image_message(message):
    if message.text == "выход":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        chat_gpt = types.KeyboardButton("ChatGPT")
        image = types.KeyboardButton("Сгенерить фото")
        markup.add(chat_gpt, image)
        bot.send_message(message.chat.id, "Выход", reply_markup=markup)

    else:
        bot.register_next_step_handler(message, handle_image_message)  # Зарегистрируйте правильную функцию для следующего шага

        resp = Client.create_generation("pollinations", message.text)
        bot.send_photo(message.chat.id, BytesIO(resp))


bot.infinity_polling()

bot.polling(none_stop=True)
