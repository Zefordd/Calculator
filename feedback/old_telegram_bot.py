import asyncio
import requests
from aiohttp import ClientSession

from models.feedback import Feedback_model

BOT_TOKEN = '541643448:AAHPmSYB_kn5zEz0cRtq76BiA6QCD8byfPY'
CHAT_ID = "386109719"
URL = "https://api.telegram.org/bot{}".format(BOT_TOKEN)


async def get_updates():
    url = URL + '/getupdates'
    r = requests.get(url)
    return r.json()


async def get_message():
    data = await get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']

    message = {"chat_id": chat_id,
                "text": message_text,}   
    return  message


async def json_post(url, json_data):
    async with ClientSession() as session:
        try:
            return await session.post(url, json=json_data)
        except Exception as e:
            print("post error: '{}'".format(str(e)))



async def post_message(bot_token, chat_id, text, reply_id=None):
    url = URL + "/sendmessage"
    json_data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_id:
        json_data["reply_to_message_id"] = reply_id

    return await json_post(url, json_data)


async def post_fact():
    i = 0
    post_msg = ''
    while True:
        i += 1
        try: 
            await Feedback_model.get_feedback(i)
            feedback = await Feedback_model.get_feedback(i)
            name, surname, feedback_text, _id = feedback['name'], feedback['surname'], feedback['feedback_text'], feedback['_id']
            post = f"{_id} FROM: {name} {surname}:\r\n\rFEEDBACK: {feedback_text}"
            post_msg += f"{post}\n\n\n"
        except AttributeError: break
    await post_message(BOT_TOKEN, CHAT_ID, post_msg)
        
async def activate_bot():
    answer = await get_message()
    message = answer['text']
    if 'go' in message:
        await post_fact()




