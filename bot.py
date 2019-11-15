# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='971587668:AAEir5pwPlOKt0hUhyZD1rLjgiCmMOlJt3Y', use_context=True) # Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здорово, школота, я Стас.')
def textMessage(update, context):
    request = apiai.ApiAI('b86f217688a24391b32c7a5cb30d79d6').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'StasManBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Не понял тебя. Перефразируй или отъебись.')
# Хендлеры
start_handler = CommandHandler('start', start)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()

