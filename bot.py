import telebot
import os
import re
from config import TOKEN
from payout import payout, payoutDict
from platforms import platforms
from api import getUser, updateUsers, getOrders, setLocation, takeOrder, updatePayout, getPayment
from state import State
from pages import orderPage, mainPage, paymentPage
from keyboards import create_main_keyboard, create_order_keyboard, create_payout_keyboard, create_platforms_keyboard, create_change_payout_keyboard

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

state = State()

def outOrders(orders, numOrder):
    state.setOrder(orders[numOrder][3])
    state.setOrders(orders=orders, cursor=numOrder)
    return orderPage(orders[numOrder][3], orders[numOrder][2], orders[numOrder][4], orders[numOrder][0])

@bot.message_handler(commands=['start'])
def start(message):
    user = getUser(message.from_user.id)
    state.resetState()
    if (len(user) == 0):
        updateUsers(message)
        state.resetState()
        state.setInProfile(True)
        create_main_keyboard(chat_id = message.chat.id, message = 'Здесь будет инструкция')
        bot.send_message(message.chat.id, text='Добавьте локацию:')
    else:
        page = mainPage(message.from_user.username, user[0][1], user[0][0], user[0][2])
        create_main_keyboard(chat_id = message.chat.id, message = page)

@bot.message_handler(func=lambda message: message.text=='Главное меню')
def main_menu(message): 
    state.resetState()
    start(message)

@bot.message_handler(func=lambda message: message.text=='Найти заказ')
def find_orders(message): 
    state.resetState()
    state.setInOrders(True)
    create_platforms_keyboard(chat_id = message.chat.id, message = 'Выберите платформу')

@bot.message_handler(func=lambda message: message.text=='Вывод')
def payout_f(message):
    state.resetState()
    current_payment = getPayment(message.from_user.id)
    state.setInPayment(True)
    if(len(current_payment) > 0):
        create_change_payout_keyboard(chat_id = message.chat.id, message = paymentPage(current_payment[-1][0]))
    else:
        create_payout_keyboard(chat_id = message.chat.id, message = 'Выберите способ выплаты')

@bot.message_handler(content_types=['text'])
def handleText(message):
    page = ''
    if(state.getState()['in_orders']):
        if (message.text in platforms):
            orders = getOrders(platform=message.text, user_id=message.from_user.id)
            if (len(orders) > 0):
                page = outOrders(orders, 0)
            else:
                bot.send_message(chat_id=message.chat.id, text=f'Заданий на <b>{message.text}</b> нет', parse_mode="HTML")
                find_orders(message)
        if (message.text == 'Искать еще'):
            ordersDict = state.getState()['orders']
            orders, maxNum = ordersDict['ordersList'], ordersDict['lentgh']            
            numOrder = (ordersDict['cursor'] + 1) % maxNum
            page = outOrders(orders, numOrder)
        if (message.text == 'Взять заказ'):
            state.setInOrder(True)
            bot.send_message(chat_id=message.chat.id, text='Пришлите скриншот отзыва')
        if (page):
            create_order_keyboard(chat_id = message.chat.id, message = page)
    if (state.getState()['in_profile']):
        setLocation(location=message.text, id=message.from_user.id)
        main_menu(message)
    if (state.getState()['in_payment']):
        if (message.text in payout):
                state.setPayment(payoutDict[message.text]['code'])
                bot.send_message(chat_id=message.chat.id, text=payoutDict[message.text]['message'])
        elif(message.text == 'Сменить способ оплаты'):
            create_payout_keyboard(chat_id = message.chat.id, message = 'Выберите способ выплаты')
        elif(state.getState()['payment']): 
            if (state.getState()['payment'] in ['Y']):
                if(bool(re.search('^89+\d{9}', message.text))):
                    updatePayout(state.getState()['payment'] + '_' + message.text, message.from_user.id)  
                    bot.send_message(chat_id=message.chat.id, text='Споспоб оплаты успешно добавлен')
                    main_menu(message)
                else:
                    bot.send_message(chat_id=message.chat.id, text='Неверный номер телефона')
            else:
                if(bool(re.search('^89+\d{9}', message.text)) | len("".join(message.text.split())) == 16):
                    updatePayout(state.getState()['payment'] + '_' + message.text, message.from_user.id)
                    bot.send_message(chat_id=message.chat.id, text='Споспоб оплаты успешно добавлен')
                    main_menu(message)
                else:
                    bot.send_message(chat_id=message.chat.id, text='Неверный номер телефона или карты')
            
@bot.message_handler(content_types=['photo'])     
def handleImages(message):
    if (state.getState()['in_order']):
        ordersDict = state.getState()['orders']
        orderId = ordersDict['ordersList'][ordersDict['cursor']][-1]
        fileID = message.photo[-1].file_id   
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        direct = f"ksmr_bot1/orders/{state.getState()['order']}"
        if (not os.path.exists(direct)):
            os.mkdir(direct)
        try:
            with open(direct + f"/{message.from_user.id}.webp", 'wb') as new_file:
                new_file.write(downloaded_file)
            takeOrder(orderId)
            bot.send_message(chat_id=message.chat.id, text='Скриншот принят!')
            main_menu(message)
            state.setInOrder(False)
        except:
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка, сори братик, попробуй другое задание')
            find_orders(message)


if (__name__ == '__main__'):
    bot.infinity_polling()