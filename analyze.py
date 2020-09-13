#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    for k in data:
        # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")

    plt.show()
    
    
    #Calculate statistical details of the temperatures
    temps = data['temperature']
    temp_medians = temps.median()
    temp_median_global = np.nanmedian(temps)
    temp_var = temps.var()
    temp_var_global = np.nanvar(temps)
    
    print('The median temperatures of each room are (C): ')
    print(temp_medians)
    print('The global median temperature is: ' + str(temp_median_global) + '\n')
    print('The variance of these temperatures are: ')
    print(temp_var)
    print('The global variance is: ' + str(temp_var_global) + '\n')

    
    #Calculate statistical details of the occupency
    occup = data['occupancy']
    occup_medians = occup.median()
    occup_median_global = np.nanmedian(occup)
    occup_vars = occup.var()
    occup_var_global = np.nanvar(occup)
    
    print('The median occupancy of each room are: ')
    print(occup_medians)
    print('The global median occupancy is: ' + str(occup_median_global) + '\n')
    print('The variance of these occupancies are: ')
    print(occup_vars)
    print('The global variance is: ' + str(occup_var_global) + '\n')
    
    #Model the distribution functions of the sensors - temperature
    print('A histogram can provide a model of the probability distributions of the sensors \n')
    print('For safety, the data has been filtered with a 5%-95% filter, because of some extreme outliers \n')
    lab1_temps =  temps.lab1[temps.lab1 < temps.lab1.quantile(0.95)]
    lab1_temps_prime = lab1_temps[lab1_temps > lab1_temps.quantile(0.05)]
    
    class_temps =  temps.class1[temps.class1 < temps.class1.quantile(0.95)]
    class_temps_prime = class_temps[class_temps > class_temps.quantile(0.05)]
    
    office_temps =  temps.office[temps.office < temps.office.quantile(0.95)]
    office_temps_prime = office_temps[office_temps > office_temps.quantile(0.05)]
    
    fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
    axs[0].hist(lab1_temps_prime, bins = 30)
    axs[0].set_xlabel('Lab 1 Temperature (C)')
    axs[0].set_ylabel('Occurence')
    axs[1].hist(class_temps_prime, bins=30)
    axs[1].set_xlabel('Class 1 Temperature (C)')
    axs[2].hist(office_temps_prime, bins=30)
    axs[2].set_xlabel('Office Temperature (C)')
    fig.show()
    
    
    #Model the distribution functions of the sensors - Occupancy
   
    lab1_occup =  occup.lab1[occup.lab1 < occup.lab1.quantile(0.95)]
    lab1_occup_prime = lab1_occup[lab1_occup > lab1_occup.quantile(0.05)]
    
    class_occup =  occup.class1[occup.class1 < occup.class1.quantile(0.95)]
    class_occup_prime = class_occup[class_occup > class_occup.quantile(0.05)]
    
    office_occup =  occup.office[occup.office < occup.office.quantile(0.95)]
    office_occup_prime = office_occup[office_occup > office_occup.quantile(0.05)]
    
    fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
    axs[0].hist(lab1_occup_prime, bins = 5)
    axs[0].set_xlabel('Lab 1 Occupancy')
    axs[0].set_ylabel('Occurence')
    axs[1].hist(class_occup_prime, bins=5)
    axs[1].set_xlabel('Class 1 Occupancy')
    axs[2].hist(office_occup_prime, bins=5)
    axs[2].set_xlabel('Office Occupancy')
    fig.show()
    
    
    #Model the distribution functions of the sensors - CO2
    co2 = data['co2']
    lab1_co2 =  co2.lab1[co2.lab1 < co2.lab1.quantile(0.95)]
    lab1_co2_prime = lab1_co2[lab1_co2 > lab1_co2.quantile(0.05)]
    
    class_co2 =  co2.class1[co2.class1 < co2.class1.quantile(0.95)]
    class_co2_prime = class_co2[class_co2 > class_co2.quantile(0.05)]
    
    office_co2 =  co2.office[co2.office < co2.office.quantile(0.95)]
    office_co2_prime = office_co2[office_co2 > office_co2.quantile(0.05)]
    
    fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
    axs[0].hist(lab1_co2_prime, bins = 20)
    axs[0].set_xlabel('Lab 1 CO2')
    axs[0].set_ylabel('Occurence')
    axs[1].hist(class_co2_prime, bins=20)
    axs[1].set_xlabel('Class 1 CO2')
    axs[2].hist(office_co2_prime, bins=20)
    axs[2].set_xlabel('Office CO2')
    fig.show()
    
    #Calculate the time series indices, and the distribution of them
    time_difference = temps.index.to_series() - temps.index.to_series().shift()
    time_difference = time_difference[1:len(time_difference)-1]
    time_difference_mean = time_difference.dt.total_seconds().mean()
    time_difference_var = time_difference.dt.total_seconds().var()
    
    print('The mean time in between arrivals is: ' + str(time_difference_mean) + '\n')
    print('The variance in time between arrivals is: ' + str(time_difference_var) + '\n')
    print('In stochastic processes, arrivals are often modeled as poisson distributions, yielding exponential waiting times between arrivals \n')
    
    print('Assuming a lambda of 1.078, an exponential distribution would have a mean of 0.927 and a variance of 0.860, which is the case here. There is some difference due to rounding in calculations \n')
    plt.figure()
    plt.hist(time_difference.dt.total_seconds(),bins = 30)
    plt.ylabel('Occurences')
    plt.xlabel('Seconds between arrivals')
    plt.show()
    print('From the source code, the distribution is generated from an erlang waiting time with k = 1, which simplifies to exponential as expected')
    
    """
    Task 3
    """
    print('We can notify possible failures based on distance from the mean')
    lab1_temp_failed = abs(temps.lab1 - temps.lab1.mean()) > 2 * pow(temps.lab1.var(),0.5)
    if(not temps.lab1[lab1_temp_failed].empty):
        print('Potential failed sensor measurements in lab 1: \n')
        print(temps.lab1[lab1_temp_failed])
        print()
    
    class1_temp_failed = abs(temps.class1 - temps.class1.mean()) > 2 * pow(temps.class1.var(),0.5)
    if(not temps.class1[class1_temp_failed].empty):
        print('Potential failed sensor measurements in class 1: \n')
        print(temps.class1[class1_temp_failed])
        print()
        
    office_temp_failed = abs(temps.office - temps.office.mean()) > 2 * pow(temps.office.var(),0.5)
    if(not temps.office[office_temp_failed].empty):
        print('Potential failed sensor measurements in office: \n')
        print(temps.office[office_temp_failed])
        print()