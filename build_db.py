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

### Build staging table

# cheeses
cursor.execute('''
               CREATE TABLE IF NOT EXISTS cheeses(
               cheese_id INT,
               cheese TEXT,
               url TEXT,
               milk TEXT,
               country TEXT,
               region TEXT,
               family TEXT,
               type TEXT,
               fat_content TEXT,
               calcium_content TEXT,
               texture TEXT,
               rind TEXT,
               color TEXT,
               flavor TEXT,
               aroma TEXT,
               vegetarian TEXT,
               vegan TEXT,
               synonyms TEXT,
               alt_spellings TEXT,
               producers TEXT
               );
               ''') 

### Build all other tables

# fct_cheese
cursor.execute('''
               CREATE TABLE IF NOT EXISTS fct_cheese(
               cheese_id INT PRIMARY KEY,
               animal_id INT,
               country_id INT,
               cheese TEXT,
               rind_id INT,
               url TEXT,
               fat_content TEXT,
               calcium_content TEXT
               );
               ''') 

# dim_rind
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_rind(
               rind_id INT PRIMARY KEY,
               rind TEXT
               );
               ''') 

# dim_animal
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_animal(
               animal_id INT PRIMARY KEY,
               animal TEXT
               );
               ''') 

# dim_country
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_country(
               country_id INT PRIMARY KEY,
               country TEXT
               );
               ''') 

# dim_producers
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_producers(
               producers_id INT PRIMARY KEY,
               producers TEXT
               );
               ''') 

# dim_type
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_type(
               type_id INT PRIMARY KEY,
               type TEXT
               );
               ''') 

# dim_texture
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_texture(
               texture_id INT PRIMARY KEY,
               texture TEXT
               );
               ''') 

# dim_colour
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_colour(
               colour_id INT PRIMARY KEY,
               colour TEXT,
               simple_colour VARCHAR(15)
               );
               ''') 

# dim_taste
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_taste(
               taste_id INT PRIMARY KEY,
               taste TEXT
               );
               ''') 

### Populate tables

# cursor.execute('''
#                COPY cheeses(
#                cheese_id,
#                cheese,
#                url,
#                milk,
#                country,
#                region,
#                family,
#                type,
#                fat_content,
#                calcium_content,
#                texture,
#                rind,
#                color,
#                flavor,
#                aroma,
#                vegetarian,
#                vegan,
#                synonyms,
#                alt_spellings,
#                producers
#                ) 
#                 FROM '/home/andrew/programming/datasets/cheese/cheeses_processed.csv' 
#                 DELIMITER '\t' 
#                 CSV HEADER;
#                ''')

with open('/home/andrew/programming/datasets/cheese/cheeses_processed.csv') as csv_file:
    next(csv_file) # skip headers
    cursor.copy_from(csv_file, 'cheeses', sep='\t')
    conn.commit()

### ### ### ### ### ### ###

# Close the cursor and connection
cursor.close()
conn.close()
print("Connection closed. Tables created.")