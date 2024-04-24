from psycopg2 import OperationalError
import psycopg2
from decouple import config
from exceptions import BalanceErr

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

conn = create_connection(config('PGSQL_DATABASE'), config('PGSQL_USER'), config('PGSQL_PASSWORD'), config('PGSQL_HOST'), config('PGSQL_PORT'))
cursor = conn.cursor()

def getUser(user_id):
    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    user = cursor.fetchall()
    return user
def updateUsers(message):
    postgres_insert_query = """ INSERT INTO users (user_id, location, balance)
                                        VALUES (%s,%s,%s)"""
    record_to_insert = (message.from_user.id, '', 0)
    cursor.execute(postgres_insert_query, record_to_insert)    
    conn.commit()
def updateBalance(user_id, amount):
    if (amount <= getUser(user_id)[0][2]):
        cursor.execute(f"UPDATE users SET balance=balance-{amount} WHERE user_id={user_id}")    
        conn.commit()
    else:
        raise BalanceErr
def setLocation(location, id):
    cursor.execute(f"UPDATE users SET location='{location}' WHERE user_id={id}")    
    conn.commit()
def updatePayout(payout, user_id, amount):
    postgres_insert_query = """ INSERT INTO payments (user_id, requisites, amount)
                                        VALUES (%s,%s,%s)"""
    record_to_insert = (user_id, payout, amount)
    cursor.execute(postgres_insert_query, record_to_insert)
    conn.commit()
def getPayment(user_id):
    cursor.execute(f"SELECT requisites FROM payments WHERE user_id={user_id}")
    current_payment = cursor.fetchall()
    return current_payment
def getOrders(platform):
    cursor.execute(f"SELECT * FROM orders WHERE platform='{platform}' AND count>0")
    orders = cursor.fetchall()
    return orders
def takeOrder(order_id):
    cursor.execute(f"UPDATE orders SET count=count-1 WHERE id='{order_id}'")    
    conn.commit()
def updateTask(name, orderId, user_id):
    cursor.execute(f"INSERT INTO tasks (order_id, name, published, user_id) VALUES ('{orderId}', '{name}', False, {user_id})")
    conn.commit()
def countProgress(user_id): 
    cursor.execute(f"SELECT COUNT(order_id) FROM tasks WHERE user_id={user_id}")
    count = cursor.fetchone()
    return count[0]