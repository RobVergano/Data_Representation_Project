# BIG PROJECT: COVID Statistics 

Course: Data Representation  
Author: Roberto Vergano

## Project A description

The aim of this project was to create and consume RESTful APIs while using a Flask server, AJAX and a SQL database. 

For the project, I wanted to study the COVID statistics in Dublin, Galway, Cork and Limerick. I created an app able to retrieve data from the cso website (1). Particularly, data from 3 different APIs: covid rates, death cases related to COVID, and vaccination rates. After formatting the json files, the data is uploaded to the “covid” SQL database (also created by the app). Through AJAX, the flask server is able to interact with the SQL database to perform CRUD operations.

## Getting started

Download the repository with the folder "Big_Project". This folder contains a python environment with all the packages and programs to run the app.

## Prerequisites

1. Python.
2. Please see requirements.txt in Big_Project folder for packages needed. 
3. Activate MySQL server, Wampserver64 was used for this project. Username: root. No password needed.
4. Activate python environment - **".\venv\Scripts\Activate.bat"**
5. Internet browser.

## How does the app work?

1. Open "Big_Project" folder in your python environment.

2. Execute **"python Myapp.py"** - This program should execute all other programs in order to 
    - create the APIs, 
    - retrieve the data from cso webpage, 
    - connect to the SQL database, 
    - create the SQL database, 
    - check for duplicates in the SQL database,
    - upload the data to the SQL database, 
    - retrieve data from the SQL database, 
    - create plots and tables to display in the webpage,
    - create a flask server, 
    - send the data to the webpage, 
    - provide the web interface to perform CRUD operations with the SQL database
    
    **No other programs need to be executed**

3. The app should be running on **"http://127.0.0.1:5000"**

4. Webpage Login details
    - Username: data
    - Password: data

## What other programs in Big_Project folder do?

All the below programs are executed by **Myapp.py** in the following order:

1. **cso.py:** This program interacts with the cso-API to retrieve data from 3 different datasets using HTTP requests, save as a file, and format the data for posterior uses. 
2. **retrieve_data.py:** This program retrieves the required data from the formatted json files and format as a pandas dataframe.
3. **visual_data.py:** This program imports the dataframes from "retrieve_data.py" to create the plots and tables for page1.html
4. **sql.connector.py:** This program provides all the methods to connect to the SQL database, create the covid database, insert data, avoid duplicates, and execute CRUD operations.  
5. **sql_dao.py:** This program retrieves the covid rates, death cases, and vaccination rates to create the plots for the page2.html
6. **sql_queries.py:** This program stores SQL queries to be used in "sql_connector.py"

## What do the other folders contain?

1. **Templates folder**: it contains all the html files for web display.
    - login.html: This page requests authorization before moving to index.html
    - index.html: This page contains 4 buttons to move around the webpages 1,2,3,4.
    - page1.html: This page provides the content for the monthly covid statistics from 2021.
    - page2.html: This page provides the content for the covid statistics since 2020
    - page3.html: This page provides the form to add/update/delete data from the vaccination_data table from the SQL database
    - page4.html: This page provides the form to add/update/delete data from the covid_rate table from the SQL database.

2. **static folder**: it contains all the png files created by visual_data.py and sql_dao.py

3. **cso folder**: it contains all the json files saved by cso.py.

## References
1. https://www.cso.ie/en/databases/  