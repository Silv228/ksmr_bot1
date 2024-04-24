def decoder_payment(payment):
    match(payment[0]):
        case('Y'):
            return f'''
<b>Юмани</b>
<code>{payment[2:]}</code>
            '''
        case('S'):
            return f'''
<b>Сбербанк</b>
<code>{payment[2:]}</code>
            '''
        case('T'):
            return f'''
<b>Тинкофф</b>
<code>{payment[2:]}</code>
            '''

def mainPage(username, id, balance, location, progress = 0): 
    return (f'''
MAIN MENU
            
<i>{username}</i> 
id: <code>{id}</code> 
Баланс: {balance} ₽
На проверке: {progress}

Локация: {location}''')

def orderPage(order_name, price, link, platform):
    return(f'''
[{platform}]
           
{order_name} 
{link} 
{price} ₽''')

def paymentPage(payment):
    return(f'''
Текущий вариант оплаты:         
{decoder_payment(payment)}
''')