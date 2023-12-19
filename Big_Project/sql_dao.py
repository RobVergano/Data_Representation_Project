# sql_dao.py
# Author: Roberto Vergano
# This program retrieves the covid rates, death cases, and vaccination rates to create the plots for the page2.html

from sql_connector import create_connection
import pandas as pd
import matplotlib.pyplot as plt

connection = create_connection(host_name='localhost', user_name='root', user_password='', db_name='covid')

# retrieve_covid_rates function: This function retrieves the covid rates from the sql database.
def retrieve_covid_rates(connection,county):
    cursor = connection.cursor()
    query = """
    SELECT date, casesper100k from covid_rates where city = %s;
    """
    values = (county, )
    cursor.execute(query,values)
    results = cursor.fetchall()
    cursor.close()
    return results 

# create_covid_rates_plot function: This function creates the plot for the covid rates.
def create_covid_rates_plot():

    Dublin = "Dublin City"
    Galway = "Galway County"
    Cork = "Cork County"
    Limerick = "Limerick City and County"

    d_cr_df = pd.DataFrame(retrieve_covid_rates(connection,Dublin), columns=['Date', 'CasesPer100k'])
    g_cr_df = pd.DataFrame(retrieve_covid_rates(connection,Galway), columns=['Date', 'CasesPer100k'])
    c_cr_df = pd.DataFrame(retrieve_covid_rates(connection,Cork), columns=['Date', 'CasesPer100k'])
    l_cr_df = pd.DataFrame(retrieve_covid_rates(connection,Limerick), columns=['Date', 'CasesPer100k'])

    d_cr_df['Date'] = pd.to_datetime(d_cr_df['Date'])
    g_cr_df['Date'] = pd.to_datetime(g_cr_df['Date'])
    c_cr_df['Date'] = pd.to_datetime(c_cr_df['Date'])
    l_cr_df['Date'] = pd.to_datetime(l_cr_df['Date'])

    plt.figure(figsize=(12, 6))
    plt.plot(d_cr_df['Date'], d_cr_df['CasesPer100k'], label='Dublin City')
    plt.plot(g_cr_df['Date'], g_cr_df['CasesPer100k'], label='Galway County')
    plt.plot(c_cr_df['Date'], c_cr_df['CasesPer100k'], label='Cork County')
    plt.plot(l_cr_df['Date'], l_cr_df['CasesPer100k'], label='Limerick City and County')

    plt.xlabel('Date')
    plt.ylabel('Cases per 100k')
    plt.title('COVID-19 Cases Evolution Over Time')
    plt.legend()
    plt.grid(True)
    
    plt.gcf().autofmt_xdate()
    plt.savefig("static\plots\covid_rates.png")
    print("Covid Rates plot saved")

# retrieve_death_rates function: This function retrieves the death rates from the sql database.
def retrieve_death_rates(connection,county):
    cursor = connection.cursor()
    query = """
    SELECT date, deaths from death_rates where county = %s;
    """
    values = (county, )
    cursor.execute(query,values)
    results = cursor.fetchall()
    cursor.close()
    return results 

# create_death_rates_plot function: This function creates the plot for the death rates.
def create_death_rates_plot():

    Dublin = "Co. Dublin"
    Galway = "Co. Galway "
    Cork = "Co. Cork"
    Limerick = "Co. Limerick"    

    d_dr_df = pd.DataFrame(retrieve_death_rates(connection,Dublin), columns=['date', 'deaths'])
    g_dr_df = pd.DataFrame(retrieve_death_rates(connection,Galway), columns=['date', 'deaths'])
    c_dr_df = pd.DataFrame(retrieve_death_rates(connection,Cork), columns=['date', 'deaths'])
    l_dr_df = pd.DataFrame(retrieve_death_rates(connection,Limerick), columns=['date', 'deaths'])

    d_dr_df['date'] = pd.to_datetime(d_dr_df['date'])
    g_dr_df['date'] = pd.to_datetime(g_dr_df['date'])
    c_dr_df['date'] = pd.to_datetime(c_dr_df['date'])
    l_dr_df['date'] = pd.to_datetime(l_dr_df['date'])

    
    plt.figure(figsize=(12, 6))
    plt.plot(d_dr_df['date'], d_dr_df['deaths'], label='Dublin City')
    plt.plot(g_dr_df['date'], g_dr_df['deaths'], label='Galway County')
    plt.plot(c_dr_df['date'], c_dr_df['deaths'], label='Cork County')
    plt.plot(l_dr_df['date'], l_dr_df['deaths'], label='Limerick City and County')
    plt.xlabel('date')
    plt.ylabel('deaths')
    plt.title('COVID-19 Deaths Evolution Over Time')
    plt.legend()
    plt.grid(True)    
    plt.gcf().autofmt_xdate()
    plt.savefig("static\plots\death_rates.png")
    print("Death rates plot saved")

# retrieve_vaccination_rates function: This function retrieves the vaccination rates from the sql database.
def retrieve_vaccination_rates(connection,county):
    cursor = connection.cursor()
    query = """
    SELECT DATE_FORMAT(Date, '%Y-%m') as YearMonth, SUM(VaccinationRate) as TotalVaccinations
    FROM vaccination_data
    WHERE city = %s
    GROUP BY DATE_FORMAT(Date, '%Y-%m');
    """
    values = (county, )
    cursor.execute(query,values)
    results = cursor.fetchall()
    cursor.close()
    return results 

# create_vaccination_rates_plots function: This function creates the plot for the vaccination rates.
def create_vaccination_rates_plots():
    Dublin = "Dublin"
    Galway = "Galway"
    Cork = "Cork"
    Limerick = "Limerick"

    

    d_vr_df = pd.DataFrame(retrieve_vaccination_rates(connection,Dublin), columns=['YearMonth', 'TotalVaccinations'])
    g_vr_df = pd.DataFrame(retrieve_vaccination_rates(connection,Galway), columns=['YearMonth', 'TotalVaccinations'])
    c_vr_df = pd.DataFrame(retrieve_vaccination_rates(connection,Cork), columns=['YearMonth', 'TotalVaccinations'])
    l_vr_df = pd.DataFrame(retrieve_vaccination_rates(connection,Limerick), columns=['YearMonth', 'TotalVaccinations'])

    # Make sure the 'Date' columns are in datetime format for proper plotting
    d_vr_df['YearMonth'] = pd.to_datetime(d_vr_df['YearMonth'])
    g_vr_df['YearMonth'] = pd.to_datetime(g_vr_df['YearMonth'])
    c_vr_df['YearMonth'] = pd.to_datetime(c_vr_df['YearMonth'])
    l_vr_df['YearMonth'] = pd.to_datetime(l_vr_df['YearMonth'])

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.plot(d_vr_df['YearMonth'], d_vr_df['TotalVaccinations'], label='Dublin City')
    plt.plot(g_vr_df['YearMonth'], g_vr_df['TotalVaccinations'], label='Galway County')
    plt.plot(c_vr_df['YearMonth'], c_vr_df['TotalVaccinations'], label='Cork County')
    plt.plot(l_vr_df['YearMonth'], l_vr_df['TotalVaccinations'], label='Limerick City and County')

    plt.xlabel('Date')
    plt.ylabel('VaccinationRate')
    plt.title('Vaccination Rate Evolution Over Time')
    plt.legend()
    plt.grid(True)

    # Adjust x-axis date format for better readability
    plt.gcf().autofmt_xdate()
    plt.savefig("static\plots\\vaccination_rates.png")
    print("Vaccination rates plot saved")




