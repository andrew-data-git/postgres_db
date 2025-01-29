import pandas as pd
import numpy as np
import psycopg2

HOST = 'localhost'
DATABASE = 'cheese_db'
USER = 'andrew'
SECRET = 'postgres'
PORT = '5432'

try:
    conn = psycopg2.connect(
        host=HOST, 
        database=DATABASE, 
        user=USER, 
        password=SECRET, 
        port=PORT)
    print("Success!")

except psycopg2.Error as e:
    print("An error occurred while connecting to the database:")
    print(e)

### ### ### ### ### ### ###

cursor = conn.cursor()
conn.autocommit = True