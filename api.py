from psycopg2 import OperationalError
import psycopg2

from config import PGSQL_DATABASE
from config import PGSQL_HOST
from config import PGSQL_PORT
from config import PGSQL_PASSWORD
from config import PGSQL_USER

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


def getUser(message):
    cursor.execute(f"SELECT * FROM users WHERE user_id={message.from_user.id}")
    user = cursor.fetchall()
    return user

def updateUsers(message):
    postgres_insert_query = """ INSERT INTO users (user_id, balance, location)
                                        VALUES (%s,%s,%s)"""
    record_to_insert = (message.from_user.id, 0, '')
    cursor.execute(postgres_insert_query, record_to_insert)    
    conn.commit()
def getOrders(platform):
    cursor.execute(f"SELECT * FROM orders WHERE platform='{platform}' AND location IS NULL")
    orders = cursor.fetchall()
    return orders