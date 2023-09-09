import psycopg2
import os
#from en_variable.set_env import set_env
#set_env()
def db_connection():
    try:
        conn=psycopg2.connect( 
            user='postgres',
            host='localhost',
            database='BeyondTheSeas',
            password='1234',
            port= 5432)
    except Exception as e:
        print(e)
    return conn