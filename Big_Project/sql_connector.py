# sql.connector.py
# Author: Roberto Vergano
# This program provides all the methods to connect to the SQL database, create the covid database, insert data, avoid duplicates, and execute CRUD operations.  

import mysql.connector
from mysql.connector import Error
import sql_queries as sq
import retrieve_data as rd
import pandas as pd
import numpy as np

#Function to create the database:
def create_database():
    database_query = sq.coviddb
    try:
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )

        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        if 'covid' not in [db[0] for db in cursor]:
            cursor.execute(database_query)        
            print("Connection to MySQL DB successful")
            print("Covid Database created successfully")
        else:
            print("Covid database already exists")

        cursor.close()

    except Error as e:
        print(f"The error '{e}' occurred")
    
# Function to create a connection to the MySQL database once the database has been created.
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to create a table in the database
def create_table(connection, create_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print(f"Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Funtion to avoid duplicated data in tables from SQL database.
def avoid_duplicates(connection, duplicate_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(duplicate_table_query)
        print("No duplicates found")
    except Error as e:
        print(f"The error '{e}' occurred")

# Functions to insert the pandas dataframes into the SQL database
def insert_covid_rates(connection):
    cursor = connection.cursor()
    covid_data = """
    INSERT IGNORE INTO covid_rates (City, Date, CasesPer100k) values (%s,%s,%s)
    ;
    """
    # Correcting the date format
    rd.weekly_covid_rates['Date'] = rd.weekly_covid_rates['Date'].str.replace(r'(\d{4} [a-zA-Z]+)(\d{2})', r'\1 \2', regex=True)
    rd.weekly_covid_rates['Date'] = pd.to_datetime(rd.weekly_covid_rates['Date']).dt.date

    # Ensure all NaN values are converted to None (Otherwise data cannot be exported)
    rd.weekly_covid_rates = rd.weekly_covid_rates.replace({np.nan: None})

    for index, row in rd.weekly_covid_rates.iterrows():
        values = (row['City'], row['Date'], row['CasesPer100k'])
        cursor.execute(covid_data, values)

    connection.commit()
    cursor.close()
    print("Data inserted successfully into the 'covid_rates' table.")

def insert_death_rates(connection):
    cursor = connection.cursor()
    death_data = """
    INSERT IGNORE INTO death_rates (County, Date, Deaths) values (%s,%s,%s)
    ;
    """
    rd.weekly_death_rates['Date'] = rd.weekly_death_rates['Date'].str.replace(r'(\d{4} [a-zA-Z]+)(\d{2})', r'\1 \2', regex=True)
    rd.weekly_death_rates['Date'] = pd.to_datetime(rd.weekly_death_rates['Date'])
    rd.weekly_death_rates = rd.weekly_death_rates.replace({np.nan: None})
    for index, row in rd.weekly_death_rates.iterrows():
        values = (row['County'], row['Date'], row['Deaths'])
        cursor.execute(death_data, values)
    connection.commit()
    cursor.close()
    print("Data inserted successfully into the 'death_rates' table.")

def insert_vaccination_rates(connection):

    cursor = connection.cursor()
    vaccination_data = """
    INSERT IGNORE INTO vaccination_data (City, Area, Date, VaccinationRate) VALUES (%s, %s, %s, %s);
    """
    date_format = "%Y %B"  
    rd.weekly_vaccination_rates['Date'] = pd.to_datetime(rd.weekly_vaccination_rates['Date'], format=date_format, errors='coerce')
    rd.weekly_vaccination_rates['Date'] = rd.weekly_vaccination_rates['Date'].dt.strftime('%Y-%m-%d')
    rd.weekly_vaccination_rates = rd.weekly_vaccination_rates.replace({np.nan: None})

    for index, row in rd.weekly_vaccination_rates.iterrows():
        values = (row['City'], row['Area'], row['Date'], row['VaccinationRate'])
        cursor.execute(vaccination_data, values)

    connection.commit()
    cursor.close()
    print("Data inserted successfully into the 'vaccination_data' table.")

# Function create_and_insert: it executes all previous functions. 
def create_and_insert():
    
    # Connect to the MySQL database
    host_name = 'localhost'
    db_name = 'covid'
    user_name = 'root'
    user_password = ''
    connection = create_connection(host_name, user_name, user_password, db_name)

    create_table(connection, sq.covid_table)
    create_table(connection, sq.deaths_table)
    create_table(connection, sq.vaccination_table)
    avoid_duplicates(connection, sq.covid_dup)
    avoid_duplicates(connection, sq.death_dup)
    avoid_duplicates(connection, sq.vacc_dup)
    insert_covid_rates(connection)
    insert_death_rates(connection)
    insert_vaccination_rates(connection)
    
    connection.close()

# Function sql_database_set_up: this function holds all the methods to connect to the SQL database,create the database, insert the data and avoid duplications.
def sql_database_set_up():    
    create_database()
    create_and_insert()

# Functions to perform CRUD operations in the webpage
def insert_vaccination_data(city, area, date, vaccination_rate):

    try:
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)
        cursor = connection.cursor()

        query = """
        INSERT INTO vaccination_data (City, Area, Date, VaccinationRate)
        VALUES (%s, %s, %s, %s)
        """
        values = (city, area, date, vaccination_rate)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def delete_vaccination_data(record_id):

    try:
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)
        cursor = connection.cursor()

        query = "DELETE FROM vaccination_data WHERE id = %s"
        values = (record_id,)
        cursor.execute(query, values)
        connection.commit()

        # To check if the record was deleted
        if cursor.rowcount == 0:
            return False  

        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False
    
def update_vaccination_data(record_id, city, area, date, vaccination_rate):
    try:
        
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)
        cursor = connection.cursor()

        query = """
        UPDATE vaccination_data 
        SET City = %s, Area = %s, Date = %s, VaccinationRate = %s
        WHERE id = %s
        """
        values = (city, area, date, vaccination_rate, record_id)

        cursor.execute(query, values)
        connection.commit()

        # To check if the record was updated
        if cursor.rowcount == 0:
            return False  

        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False
    
def insert_covid_rates_sql(city, date, cases_per_100k):
    try:
        
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)
        
        cursor = connection.cursor()

        query = """
        INSERT INTO covid_rates (City, Date, CasesPer100k)
        VALUES (%s, %s, %s)
        """
        values = (city, date, cases_per_100k)
        cursor.execute(query, values)
        connection.commit()        
        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False
    
def update_covid_rates(record_id, city, date, cases_per_100k):
    try:
        
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)
        
        cursor = connection.cursor()
        query = """
        UPDATE covid_rates
        SET City = %s, Date = %s, CasesPer100k = %s
        WHERE id = %s
        """
        values = (city, date, cases_per_100k, record_id)        
        cursor.execute(query, values)
        connection.commit()

        # To check if the record was updated
        if cursor.rowcount == 0:
            return False  

        return True
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_covid_rates(record_id):
    try:
        
        host_name = 'localhost'
        db_name = 'covid'
        user_name = 'root'
        user_password = ''
        connection = create_connection(host_name, user_name, user_password, db_name)        
        cursor = connection.cursor()

        query = "DELETE FROM covid_rates WHERE id = %s"
        cursor.execute(query, (record_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return False
        return True
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()