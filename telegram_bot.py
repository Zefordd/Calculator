import asyncio
from aiohttp import ClientSession

import telebot
from telebot.types import Message

from models.feedback import Feedback_model


TOKEN = '541643448:AAHPmSYB_kn5zEz0cRtq76BiA6QCD8byfPY'
CHAT_ID = "386109719"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy partner!!")


def get_message():
    i = 0
    post_msg = ''
    while True:
        i += 1
        try: 
            Feedback_model.get_feedback_for_bot(i)
            feedback = Feedback_model.get_feedback_for_bot(i)
            name, surname, feedback_text, _id = feedback['name'], feedback['surname'], feedback['feedback_text'], feedback['_id']
            post = f"{_id} FROM: {name} {surname}:\r\n\rFEEDBACK: {feedback_text}"
            post_msg += f"{post}\n\n\n"
        except AttributeError: break
    return post_msg

@bot.message_handler(content_types=['text'])
def send_message(message: Message):
    if 'go' in message.text:
        post_msg = get_message()
        bot.send_message(message.chat.id, post_msg)
    else:
         bot.send_message(message.chat.id, 'Type "go" to go')


if __name__ == '__main__':
    bot.polling(none_stop=True)





