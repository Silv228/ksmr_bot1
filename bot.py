import telebot
import os
from config import TOKEN
from api import getUser, updateUsers, setLocation, takeOrder, getPayment, updateTask
from state import State
from pages import mainPage, paymentPage
from keyboards import create_main_keyboard, create_payout_keyboard, create_platforms_keyboard, create_change_payout_keyboard, reset_keyboard
from components.order import Orders_handler
from components.payout import Payout_handler, Payment_handler

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

state = State()


@bot.message_handler(commands=['start'])
def start(message):
    user = getUser(message.from_user.id)
    state.resetState()
    if (len(user) == 0):
        updateUsers(message)
        state.setInProfile(True)
        bot.send_message(message.chat.id, text='Добавьте локацию:')
    else:
        page = mainPage(message.from_user.username,
                        user[0][0], user[0][2], user[0][1])
        create_main_keyboard(chat_id=message.chat.id, message=page)


@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def main_menu(message):
    start(message)

@bot.message_handler(func=lambda message: message.text == 'Найти заказ')
def find_orders(message):
    state.resetState()
    state.setInOrders(True)
    create_platforms_keyboard(chat_id=message.chat.id,
                              message='Выберите платформу')

@bot.message_handler(func=lambda message: message.text == 'Вывод')
def payout_f(message):
    state.resetState()
    current_payment = getPayment(message.from_user.id)
    state.setInPayment(True)
    if (len(current_payment) > 0):
        state.setPayment(current_payment[-1][0])    
        create_change_payout_keyboard(chat_id=message.chat.id, message=paymentPage(current_payment[-1][0]))
    else:
        create_payout_keyboard(chat_id=message.chat.id, message='Выберите способ выплаты')

@bot.message_handler(content_types=['text'])
def handleText(message):
    if (state.getState()['in_orders']):
        Orders_handler(message, find_orders, state)
    if (state.getState()['in_profile']):
        setLocation(location=message.text, id=message.from_user.id)
        main_menu(message)
    if (state.getState()['in_payout']):
        Payout_handler(message, state.getState()['payment'], main_menu, state)
    if (state.getState()['in_tasks']):
        ordersDict = state.getState()['orders']
        orderId = ordersDict['ordersList'][ordersDict['cursor']][-1]
        updateTask(message.text, orderId)
        takeOrder(orderId)
        bot.send_message(chat_id=message.chat.id, text='Отзыв принят')
        main_menu(message)
    if (state.getState()['in_payment']):
        Payment_handler(message, state)


@bot.message_handler(content_types=['photo'])
def handleImages(message):
    if (state.getState()['in_order']):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        direct = f"ksmr_bot1/orders/{state.getState()['order']}"
        if (not os.path.exists(direct)):
            os.mkdir(direct)
        try:
            with open(direct + f"/{message.from_user.id}.webp", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(chat_id=message.chat.id, text='Скриншот принят!')
            reset_keyboard(chat_id=message.chat.id, message='Введите имя в отзыве')
            state.setInOrder(False)
            state.setInTasks(True)
        except:
            bot.send_message(
                chat_id=message.chat.id, text='Произошла ошибка, попробуйте другое задание')
            find_orders(message)


if (__name__ == '__main__'):
    bot.infinity_polling()
