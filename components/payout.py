import telebot
import re
from decouple import config
from payout import payout, payoutDict
from exceptions import BalanceErr
from api import getUser, updatePayout, updateBalance
from keyboards import create_payout_keyboard, reset_keyboard

bot = telebot.TeleBot(token=config('TOKEN'), parse_mode=None)

def Payout_handler(message, req, main_menu, state):
    platformFull = ''
    for i in [val if req[0] in val['code'] else 0 for val in list(payoutDict.values())]:
        if i != 0:
            platformFull = list(payoutDict.keys())[
                list(payoutDict.values()).index(i)]
    try:
        if (getUser(message.from_user.id)[0][2] < payoutDict[platformFull]['limit']):
            raise BalanceErr()
        if (int(message.text) >= payoutDict[platformFull]['limit']):
            updateBalance(message.from_user.id, int(message.text))
            updatePayout(req, message.from_user.id, int(message.text))
            bot.send_message(chat_id=message.chat.id, text='Вывод поставлен в очередь')
            main_menu(message)
        else:
            bot.send_message(chat_id=message.chat.id, 
                            text=f'Минимальный вывод через {platformFull}: {payoutDict[platformFull]["limit"]} ₽')
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text='Ошибка, проверьте правильность ввода суммы!')
    except BalanceErr:
        bot.send_message(chat_id=message.chat.id, text=BalanceErr().message)
    except Exception:
        print('err')
def Payment_handler(message, state):
    if (message.text in payout):
        state.setPayment(payoutDict[message.text]['code'])
        bot.send_message(chat_id=message.chat.id,
                         text=payoutDict[message.text]['message'])
    elif (message.text == 'Сменить способ оплаты'):
        create_payout_keyboard(chat_id=message.chat.id, message='Выберите способ выплаты')
    elif(message.text == 'Продолжить выплату'):
        reset_keyboard(chat_id=message.chat.id, message='Введите сумму')
        state.setInPayment(False)
        state.setInPayout(True)
    elif (state.getState()['payment']):
        if (bool(re.search('^(8|\+7)9+\d{9}', message.text)) or len("".join(message.text.split())) == 16):
            state.setPayment(state.getState()['payment'] + '_' + message.text)
            reset_keyboard(chat_id=message.chat.id,
                                 message='Введите сумму')
            state.setInPayment(False)
            state.setInPayout(True)
        else:
            bot.send_message(chat_id=message.chat.id,
                                 text='Неверный номер телефона или карты')
                