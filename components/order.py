from config import TOKEN
import telebot
from platforms import platforms
from api import getOrders
from pages import orderPage
from keyboards import create_order_keyboard
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)


def outOrders(orders, numOrder, state):
    state.setOrder(orders[numOrder][3])
    state.setOrders(orders, numOrder)
    return orderPage(orders[numOrder][3], orders[numOrder][2], orders[numOrder][4], orders[numOrder][0])

def Orders_handler(message, find_orders, state):
    page = ''
    if (message.text in platforms):
        orders = getOrders(platform=message.text, user_id=message.from_user.id)
        if (len(orders) > 0):
            page = outOrders(orders, 0, state)
        else:
            bot.send_message(
                chat_id=message.chat.id, text=f'Заданий на <b>{message.text}</b> нет', parse_mode="HTML")
            find_orders(message)
    if (message.text == 'Искать еще'):
        ordersDict = state.getState()['orders']
        orders, maxNum = ordersDict['ordersList'], ordersDict['lentgh']
        numOrder = (ordersDict['cursor'] + 1) % maxNum
        page = outOrders(orders, numOrder)
    if (message.text == 'Взять заказ'):
        state.setInOrder(True)
        bot.send_message(chat_id=message.chat.id,
                         text='Пришлите скриншот отзыва')
    if (page):
        create_order_keyboard(chat_id=message.chat.id, message=page)
