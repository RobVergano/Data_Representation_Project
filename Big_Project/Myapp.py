# Myapp.py
# Author: Roberto Vergano
# This program executes all the programs to retrieve data from cso.ie, create tables and plots, and create SQL database. Then it runs the Flask app and allows webpage display.

import cso
import visual_data as vs
import sql_connector as sc
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='', static_folder='static')

# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Route to process the login page
@app.route('/process_login', methods=['POST'])

# Function to process the login
def process_login():
    username = request.form['username']
    password = request.form['password']

    if username == 'data' and password == 'data':
        return redirect(url_for('main_page'))
    else:
        return 'Login Failed!'

# Route to process the index page
@app.route('/index')

def main_page():
    return render_template('index.html')

# Route to process the page 1: "Monthly Covid Statistics 2021"
@app.route('/page1')

def page1():
    return render_template('page1.html', table1=vs.dublin_stats, table2=vs.cork_stats, table3=vs.gal_stats, table4=vs.lim_stats)

# Route to process the page 2: "Monthly Evolution Since 2020"
@app.route('/page2')

def page2():
    return render_template('page2.html')

# Route to process the page 3: "App/Update/Delete Vaccination Data"
@app.route('/page3')
def page3():
    return render_template('page3.html')

# Route to execute "add_vaccination_data".
@app.route('/api/add_vaccination_data', methods=['POST'])

# Function to insert vaccination data in SQL Database
def add_vaccination_data():
    try:
        data = request.get_json()
        success = sc.insert_vaccination_data(data['city'], data['area'], data['date'], data['vaccinationRate'])
        
        if success:
            return jsonify({"message": "Data added successfully"}), 200
        else:
            return jsonify({"message": "Failed to add data"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500

# Route to execute "delete_vaccination_data".
@app.route('/api/delete_vaccination_data/<int:record_id>', methods=['DELETE'])

# Function to delete vaccination data in SQL Database
def delete_vaccination_data(record_id):
    success = sc.delete_vaccination_data(record_id)  
    if success:
        return jsonify({"message": "Record deleted successfully"}), 200
    else:
        return jsonify({"message": "Error deleting record"}), 500

# Route to execute "update_vaccination_data".
@app.route('/api/update_vaccination_data/<int:record_id>', methods=['PUT'])

# Function to update vaccination data in SQL Database
def update_vaccination_data(record_id):
    try:
        data = request.get_json()
        success = sc.update_vaccination_data(record_id, data['city'], data['area'], data['date'], data['vaccinationRate'])
        
        if success:
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update data"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500

# Route to process the page 4: "App/Update/Delete Covid Data"
@app.route('/page4')
def page4():
    return render_template('page4.html')

# Route to execute "add_covid_rates_data".
@app.route('/api/add_covid_rates_data', methods=['POST'])

# Function to add covid data in SQL Database
def add_covid_rates_data():
    data = request.json
    success = sc.insert_covid_rates_sql(data['city'], data['date'], data['casesPer100k'])
    if success:
        return jsonify({'message': 'Data added successfully'}), 200
    else:
        return jsonify({'message': 'Error adding data'}), 500

# Route to execute "update_covid_rates_data".
@app.route('/api/update_covid_rates_data/<int:record_id>', methods=['PUT'])

# Function to update covid data in SQL Database
def update_covid_rates_data(record_id):
    try:
        data = request.get_json()
        success = sc.update_covid_rates(record_id, data['city'], data['date'], data['casesPer100k'])
        
        if success:
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update data"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500

# Route to execute "delete_covid_rates_data".
@app.route('/api/delete_covid_rates_data/<int:record_id>', methods=['DELETE'])

# Function to delete covid data in SQL Database
def delete_covid_rates_data(record_id):
    success = sc.delete_covid_rates(record_id)  
    if success:
        return jsonify({"message": "Record deleted successfully"}), 200
    else:
        return jsonify({"message": "Error deleting record"}), 500

# Function Initialize_app: executes all programs to retrieve data, create and insert data in the SQL database, and create plots for the webpage.
def initialize_app():
    cso.getFormattedAsFile(cso.covid_rates, cso.covid_cso)
    cso.getFormattedAsFile(cso.death_rates, cso.death_rates_cso)
    cso.getFormattedAsFile(cso.vaccination_rates, cso.vaccination_rates_cso)
    vs.tables_and_bar_plot()
    sc.sql_database_set_up()
    import sql_dao as sd
    sd.create_covid_rates_plot()
    sd.create_death_rates_plot()
    sd.create_vaccination_rates_plots()

if __name__ == '__main__':
    initialize_app() 
    app.run(debug=False) # Due to "debug = True" the app runs twice. Fixed as "False"



