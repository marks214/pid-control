import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
from datetime import datetime, date
import numpy as np
from datetime import datetime
import csv
import time

figwidth = 10
figheight = 8
fs = 15

def model_heating(t, tau, K, C):
    return K*(1 - np.exp(np.divide(np.negative(t), tau))) + C

def model_cooling(t, tau, K, C):
    return K*(np.exp(np.divide(np.negative(t), tau))) + C

def get_heating_label(popt):
     label = r'$f(t) = $' + str(round(popt[1], 2)) + r'$(1-$' + r'$exp(-t/$' + str(round(popt[0], 2)) + r'$)) +  $' + str(round(popt[2], 2))
     print(label)
     return label

def get_cooling_label(popt):
     label =  r'$f(t) = $' + str(round(popt[1], 2)) + r'$exp(-t/$' + str(round(popt[0], 2)) + r'$) + $' + str(round(popt[2], 2))
     print(label)
     return label

def get_Params(time_values, temperature_values, start_DC, end_DC):
    if start_DC == end_DC:
        return []

    if start_DC < end_DC:
        model = model_heating
        initial_guess = (40, max(temperature_values) - temperature_values[0], temperature_values[0])
        get_label = get_heating_label
    else:
        model = model_cooling
        initial_guess = (40, max(temperature_values) - temperature_values[-1], temperature_values[-1])
        get_label = get_cooling_label

    popt, pcov = curve_fit(model, time_values, temperature_values, p0=initial_guess)
    return popt
  
    #to write: popt[0] = tau
    #popt[1] = Kp
    #popt[2] = C

results = {}

file_names = pd.DataFrame({'Data_1':{}, 'Data_2':{}, 'Data_3':{}, 'Data_4':{}, 'Data_5':{}})
for file_name in file_names:
    data = pd.read_csv(file_name + '.csv')
    data = data.reset_index(drop=True) # reset the index
    data = data.reset_index()

    full_time_values = data['time']
    full_temperature_values = data['temperature']
    full_dc_values = data['DC']

    time_values = [0]
    temperature_values = [25]
    start_time = 0
 
    # with open(file_name, 'a', newline='') as csvfile:
    #     temperaturewriter = csv.writer(csvfile, delimiter=',')
    #     temperaturewriter.writerow(['Trial', 'DC', 'Kp', 'tau'])
    start_DC = 0
    for i in range(1, len(full_time_values)):
        last_DC_value = full_dc_values[i-1]
        current_DC_value = full_dc_values[i]
        if abs(last_DC_value - current_DC_value) > 0 :
            popt = get_Params(time_values, temperature_values, start_DC, last_DC_value)
            if len(popt) == 0:
                continue
            dc_delta = str(last_DC_value - start_DC)
            if not file_name in results:
                results[file_name] = {}
            if not dc_delta in results[file_name]:
                results[file_name][dc_delta] = {}

            results[file_name][dc_delta]['tau'] = popt[0]
            results[file_name][dc_delta]['kp'] = popt[1]
            results[file_name][dc_delta]['c']= popt[2]

            start_time = full_time_values[i]
            start_DC = last_DC_value

            time_values = [full_time_values[i] - start_time]
            temperature_values = [full_temperature_values[i]]
        else:
            time_values.append(full_time_values[i] - start_time)
            temperature_values.append(full_temperature_values[i])
get_Params(time_values, temperature_values, start_DC, last_DC_value)


run()