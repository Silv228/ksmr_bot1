from psycopg2 import OperationalError
import psycopg2

from config import PGSQL_DATABASE, PGSQL_HOST, PGSQL_PORT, PGSQL_PASSWORD, PGSQL_USER

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

conn = create_connection(PGSQL_DATABASE, PGSQL_USER, PGSQL_PASSWORD, PGSQL_HOST, PGSQL_PORT)
cursor = conn.cursor()

def getUser(user_id):
    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    user = cursor.fetchall()
    return user

def updateUsers(message):
    postgres_insert_query = """ INSERT INTO users (user_id, balance, location)
                                        VALUES (%s,%s,%s)"""
    record_to_insert = (message.from_user.id, 0, '')
    cursor.execute(postgres_insert_query, record_to_insert)    
    conn.commit()
def setLocation(location, id):
    cursor.execute(f"UPDATE users SET location='{location}' WHERE user_id={id}")    
    conn.commit()
def updatePayout(payout, user_id, amount=0):
    postgres_insert_query = """ INSERT INTO payments (user_id, requisites, amount)
                                        VALUES (%s,%s,%s)"""
    record_to_insert = (user_id, payout, amount)
    cursor.execute(postgres_insert_query, record_to_insert)
    conn.commit()
def getPayment(user_id):
    cursor.execute(f"SELECT requisites FROM payments WHERE user_id={user_id}")
    current_payment = cursor.fetchall()
    return current_payment
def getOrders(platform, user_id):
    # location=(SELECT location FROM users WHERE user_id={user_id}) AND
    cursor.execute(f"SELECT * FROM orders WHERE platform='{platform}' AND count>0")
    orders = cursor.fetchall()
    return orders
def takeOrder(order_id):
    cursor.execute(f"UPDATE orders SET count=count-1 WHERE id='{order_id}'")    
    conn.commit()