# cso.py
# Author: Roberto Vergano
# This program interacts with the cso-API to retrieve data from 3 different datasets using HTTP requests, save as a file, and format the data for posterior uses. 

import requests
import json

# cso URL:
urlbegining = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlend ="/JSON-stat/2.0/en"

# Datasets from cso.ie:
covid_rates = "CRW02"
death_rates = "CDC05"
vaccination_rates = "CDC47"

# json paths
covid_cso = "cso\covid_formatted.json"
death_rates_cso = "cso\death_formatted.json"
vaccination_rates_cso = "cso\\vaccination_formatted.json"

# Function getall: It makes an HTTP GET request to the constructed URL to retrieve the dataset from the CSO-API. Returns a json response.
def getAll(dataset):
    url = urlbegining + dataset + urlend
    response = requests.get(url)
    return response.json()

# Function getAllasFIle: It takes the json response from getall() and saves it in a json file.
def getAllasFile(dataset):
    with open("cso\cso.json", "wt") as fp:
            json_data = json.dumps(getAll(dataset), indent=4)  
            print(json_data, file=fp)    

# Function getFormatted: it formats the json response for an easier interpretation and manipulation.
def getFormatted(dataset):
    data = getAll(dataset)
    ids = data["id"]
    values =data["value"]
    dimensions = data["dimension"]
    sizes = data["size"]
    valuecount = 0
    result = {}
    
    for dim0 in range(sizes[0]):
        currentId = ids[0]
        index = list(dimensions[currentId]["category"]["index"])[dim0]
        stat_label = dimensions[currentId]["category"]["label"][index]
        result[stat_label] = {}

        for dim1 in range(sizes[1]):
            currentId = ids[1]
            index = list(dimensions[currentId]["category"]["index"])[dim1]
            date_label = dimensions[currentId]["category"]["label"][index]
            result[stat_label][date_label] = {}

            for dim2 in range(sizes[2]):
                currentId = ids[2]
                index = list(dimensions[currentId]["category"]["index"])[dim2]
                county_label = dimensions[currentId]["category"]["label"][index]
                result[stat_label][date_label][county_label] = values[valuecount]
                valuecount += 1
    
    return result

# Function getFormattedAsFile: it saves the formatted dataset in a new json file for later use.
def getFormattedAsFile(dataset,formatted_cso):
    with open(formatted_cso, "wt") as fp:
            json_data = json.dumps(getFormatted(dataset), indent=4)  
            print(json_data, file=fp)
            print("Json files saved")

if __name__ == "__main__":
    getFormattedAsFile(covid_rates,covid_cso)
    getFormattedAsFile(death_rates,death_rates_cso)
    getFormattedAsFile(vaccination_rates,vaccination_rates_cso)

