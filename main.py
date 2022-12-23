from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Adafruit_IO import Client, Data
import os
import requests

def turnoffthelight(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bulb turned1 off")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://pngimg.com/uploads/bulb/bulb_PNG1241.png')
    send_value(0)


def turnonthelight(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bulb turned on")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://img.icons8.com/plasticine/2x/light-on.png')
    send_value(1)


def ler_temperatura(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Leitura dda Temperatura")
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_value()[3] + " ºC")
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo='https://img.icons8.com/external-kosonicon-flat-kosonicon/344/external-temperatures-temperature-kosonicon-flat-kosonicon.png')
    # send_value(1)


def busca_gato(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="gatott")
    data = requests.get("https://api.thecatapi.com/v1/images/search")
    vurl = data.json()[0]['url']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=vurl)


def send_value(value):
    feed = aio.feeds('luz')
    aio.send_data(feed.key, value)


def get_value():
    feed = aio.feeds('temperatura')
    ret = aio.receive(feed.key)
    return ret


def input_message(update, context):
    text = update.message.text
    if text == 'turnonthelight':
        send_value('1')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bulb turned 2on")
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo='https://img.icons8.com/plasticine/2x/light-on.png')
    elif text == 'turnoffthelight':
        send_value('0')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bulb turned off")
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo='https://pngimg.com/uploads/bulb/bulb_PNG1241.png')
    elif (text == 'ler' or text == 'Ler'):
        # ler_temperatura2()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Opa")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Leitura da Temperatura")
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_value()[3] + " ºC")
    elif text == 'gato' or text == 'Gato':
        # ler_temperatura2()
        # context.bot.send_message(chat_id=update.effective_chat.id,text="Opast gato")
        data = requests.get("https://api.thecatapi.com/v1/images/search")
        vurl = data.json()[0]['url']
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=vurl)


def start(update, context):
    start_message = '''
/turnoff the light or 'turn off':To turn off the bulb ,sends andre value=0 in feed
/turnon the light or 'turn on'  :To turn on the bulb ,sends value=1 in feed
/ler Temperatura  :pega leitura do termometro feed
/gato fotos de gatos
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


# ADAFRUIT_IO_USERNAME =  os.getenv('andreluizgois')
# ADAFRUIT_IO_KEY = os.getenv('aio_vRQS09b2v3mXXgLoAli2Axj9YZcw')
ADAFRUIT_IO_USERNAME = 'andreluizgois'
ADAFRUIT_IO_KEY = 'aio_vRQS09b2v3mXXgLoAli2Axj9YZcw'
TOKEN = os.getenv('5538229015:AAHTlwuqqZSJcy-kI0i2RbJqI0quaDCuHe0')
TOKEN = '5538229015:AAHTlwuqqZSJcy-kI0i2RbJqI0quaDCuHe0'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('turnoff', turnoffthelight))
dispatcher.add_handler(CommandHandler('turnon', turnonthelight))
dispatcher.add_handler(CommandHandler('menu', start))
dispatcher.add_handler(CommandHandler('ler', ler_temperatura))
dispatcher.add_handler(CommandHandler('gato', busca_gato))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), input_message))
updater.start_polling()

updater.idle()

