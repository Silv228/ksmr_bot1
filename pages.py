def mainPage(username, id, balance): 
    return (f'{username} \nid: {id} \nБаланс: {balance}')

def orderPage(order_name, price, link, platform):
    return(f'[{platform}] \n{order_name} \n{link} \n{price} ')