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

# dim_rind
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_rind(
               rind_id SERIAL PRIMARY KEY,
               rind TEXT
               );
               ''') 

# dim_animal
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_animal(
               animal_id SERIAL PRIMARY KEY,
               animal TEXT
               );
               ''') 

# dim_country
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_country(
               country_id SERIAL PRIMARY KEY,
               country TEXT
               );
               ''') 

# dim_producers
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_producers(
               producers_id SERIAL PRIMARY KEY,
               producers TEXT
               );
               ''') 

# dim_type
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_type(
               type_id SERIAL PRIMARY KEY,
               type TEXT
               );
               ''') 

# dim_texture
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_texture(
               texture_id SERIAL PRIMARY KEY,
               texture TEXT
               );
               ''') 

# dim_colour
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_colour(
               colour_id SERIAL PRIMARY KEY,
               colour TEXT,
               simple_colour VARCHAR(15)
               );
               ''') 

# dim_taste
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_taste(
               taste_id SERIAL PRIMARY KEY,
               taste TEXT
               );
               ''') 

# dim_cheese
cursor.execute('''
               CREATE TABLE IF NOT EXISTS dim_cheese(
               cheese_id SERIAL PRIMARY KEY,
               animal_id INT,
               country_id INT,
               cheese TEXT,
               rind_id INT,
               url TEXT,
               fat_content TEXT,
               calcium_content TEXT
               );
               ''') 

### Populate cheeses

cursor.execute('''TRUNCATE TABLE cheeses RESTART IDENTITY''')
with open('/home/andrew/programming/datasets/cheese/cheeses_processed.csv') as csv_file:
    next(csv_file) # skip headers
    cursor.copy_from(csv_file, 'cheeses', sep='\t')
    conn.commit()

### ### ### ### ### ### ###

# 1. Extract unique values from the cheeses table to populate your dim_cheese and dim_animal dimension tables.
# 2. Insert the unique values into the dimension tables.
# 3. Populate the fact table or update the original cheeses table to use the new dimension table keys.

# 1.1
# INSERT INTO dim_cheese (cheese_name, cheese_type, cheese_flavor_profile)
# SELECT DISTINCT cheese_name, cheese_type, cheese_flavor_profile
# FROM cheeses
# ON CONFLICT (cheese_name) DO NOTHING;

# 1.2
# INSERT INTO dim_animal (animal_type)
# SELECT DISTINCT animal_type
# FROM cheeses
# WHERE animal_type IS NOT NULL
# ON CONFLICT (animal_type) DO NOTHING;


# Step 2: Populate the Fact Table with Foreign Keys

# Once the dimension tables are populated, you'll need to link them back to the cheeses table (or insert them into a fact 
# table, depending on your use case). To do this, we will update the cheeses table (or use a fact table) to reference the 
# keys from dim_cheese and dim_animal.

# Assuming you want to update the cheeses table with the cheese_id and animal_id from the dimension tables, you can 
# run the following updates.
# 2.1 Update cheeses Table with Foreign Keys

# -- Update the cheeses table with the cheese_id from dim_cheese
# UPDATE cheeses
# SET cheese_id = dc.cheese_id
# FROM dim_cheese dc
# WHERE cheeses.cheese_name = dc.cheese_name;

# -- Update the cheeses table with the animal_id from dim_animal
# UPDATE cheeses
# SET animal_id = da.animal_id
# FROM dim_animal da
# WHERE cheeses.animal_type = da.animal_type;

# These UPDATE queries will:

#     Link the cheeses table to the dim_cheese and dim_animal dimension tables.
#     Use the cheese_name and animal_type columns to match the corresponding records in the dimension 
# tables and update the cheese_id and animal_id foreign keys in the cheeses table.





### ### ### ### ### ### ###

# Close the cursor and connection
cursor.close()
conn.close()
print("Connection closed. Tables created.")