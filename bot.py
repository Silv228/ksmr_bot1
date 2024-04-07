import telebot
from config import TOKEN
from payout import payout
from platforms import platforms
from api import getUser, updateUsers, getOrders, setLocation
from state import State
from pages import orderPage, mainPage

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

state = State()

def create_main_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    find_offer = telebot.types.KeyboardButton(text="Найти заказ")
    keyboard.add(find_offer)
    payout = telebot.types.KeyboardButton(text="Вывод")
    keyboard.add(payout)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_order_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    getOffer = telebot.types.KeyboardButton(text="Взять заказ")
    keyboard.add(getOffer)
    findNext = telebot.types.KeyboardButton(text="Искать еще")
    keyboard.add(findNext)
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_payout_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for i in payout:    
        keyboard.add(telebot.types.KeyboardButton(text=i))
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_platforms_keyboard(chat_id, message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for i in platforms: 
        keyboard.add(telebot.types.KeyboardButton(text=i))
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    user = getUser(message)
    state.resetState()
    print(user)
    if (len(user) == 0):
        updateUsers(message)
        state.resetState()
        state.setProfile(True)
        bot.send_message(message.chat.id, text='Добавьте локацию:')
        create_main_keyboard(chat_id = message.chat.id, message = 'Здесь будет инструкция')
    else:
        page = mainPage(message.from_user.username, user[0][1], user[0][0], user[0][2])
        create_main_keyboard(chat_id = message.chat.id, message = page)

@bot.message_handler(func=lambda message: message.text=='Главное меню')
def main_menu(message): 
    state.resetState()
    create_main_keyboard(chat_id = message.chat.id, message = 'Главное меню')

@bot.message_handler(func=lambda message: message.text=='Найти заказ')
def find_orders(message): 
    state.setOrder(True)
    create_platforms_keyboard(chat_id = message.chat.id, message = 'Выберите платформу')
    
@bot.message_handler(content_types=['text'])
def find_order(message):
    if(state.getState()['in_order']):
        if (message.text in platforms):
            ordres = getOrders(message.text)
            page = orderPage(ordres[0][3], ordres[0][2], ordres[0][4], ordres[0][0])
            create_order_keyboard(chat_id = message.chat.id, message = page)
    if(state.getState()['in_profile']):
        setLocation(location=message.text, id=message.from_user.id)
        
@bot.message_handler(func=lambda message: message.text=='Вывод')
def payout_f(message):
    create_payout_keyboard(chat_id = message.chat.id, message = 'Выберите способ выплаты')

if (__name__ == '__main__'):
    bot.infinity_polling()