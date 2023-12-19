# sql_queries.py
# This program stores SQL queries to be used in "sql_connector.py"

# SQL Query to create database:
coviddb = """
    CREATE DATABASE IF NOT EXISTS covid;
    """
# SQL Queries to create the tables   
covid_table = """
    CREATE TABLE IF NOT EXISTS covid_rates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(100) NOT NULL,
        Date DATE NOT NULL,
        CasesPer100k FLOAT
    );
"""

deaths_table = """    
    CREATE TABLE IF NOT EXISTS death_rates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        County VARCHAR(100) NOT NULL,
        Date DATE NOT NULL,
        Deaths INT
    );    
"""

vaccination_table = """
    CREATE TABLE IF NOT EXISTS vaccination_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(100) NOT NULL,
        Area VARCHAR(100) NOT NULL,
        Date DATE NOT NULL,
        VaccinationRate FLOAT
    );
"""
# SQL Queries to avoid duplicates:

covid_dup = """
    ALTER TABLE covid_rates
    ADD UNIQUE KEY unique_index (City,Date,CasesPer100k);
    """

death_dup = """
    ALTER TABLE death_rates
    ADD UNIQUE KEY unique_index (County,Date,Deaths);
    """

vacc_dup = """
    ALTER TABLE vaccination_data
    ADD UNIQUE KEY unique_index (City, Area, Date, VaccinationRate);
    """

