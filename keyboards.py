import telebot
from platforms import platforms
from payout import payout
from config import TOKEN

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

def create_main_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    find_offer = telebot.types.KeyboardButton(text="Найти заказ")
    keyboard.add(find_offer)
    payout = telebot.types.KeyboardButton(text="Вывод")
    keyboard.add(payout)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard, parse_mode='HTML')

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

def create_change_payout_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    payout = telebot.types.KeyboardButton(text="Продолжить выплату")
    keyboard.add(payout)
    change_payment = telebot.types.KeyboardButton(text="Сменить способ оплаты")
    keyboard.add(change_payment)
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard, parse_mode='HTML')