def mainPage(username, id, balance, location): 
    return (f'{username} \nid: {id} \nБаланс: {balance} \nЛокация: {location}')

def orderPage(order_name, price, link, platform):
    return(f'[{platform}] \n{order_name} \n{link} \n{price} ')