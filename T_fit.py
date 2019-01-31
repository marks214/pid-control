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

file_name = '_Lab_on_a_Chip_plastic_1_plastic_sphere_thermal_camera1548869196.0441263'
data = pd.read_csv(file_name + '.csv')
data = data.reset_index(drop=True) # reset the index
data = data.reset_index()
data.columns

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
     
def PlotTemps(time_values, temperature_values, start_DC, end_DC):
    if start_DC == end_DC:
        return

    if start_DC < end_DC:
        model = model_heating
        initial_guess = (40, max(temperature_values) - temperature_values[0], temperature_values[0])
        get_label = get_heating_label
    else:
        model = model_cooling
        initial_guess = (40, max(temperature_values) - temperature_values[-1], temperature_values[-1])
        get_label = get_cooling_label

    popt, pcov = curve_fit(model, time_values, temperature_values, p0=initial_guess)
    plt.figure(figsize=(figwidth,figheight))
    plt.plot(time_values,temperature_values, 'm.',label='DC ' + str(start_DC) + ' to ' + str(end_DC)) # plot temp against time
    plt.plot(time_values, model(time_values, *popt), 'g', label= get_label(popt) )
    plt.legend()
    plt.ylabel('Temperature (' + r'$\degree$' +'C)',fontsize=fs)
    plt.xlabel('Time (s)',fontsize=fs)
    plt.savefig('1_plastic_sphere_dt'+ str(start_DC) +'to' + str(end_DC) + '.svg')
    

full_time_values = data['time']
full_temperature_values = data['temperature']
full_dc_values = data['DC']

time_values = [0]
temperature_values = [25]
start_time = 0

start_DC = 0
for i in range(1, len(data['time'])):
    last_DC_value = full_dc_values[i-1]
    current_DC_value = full_dc_values[i]
    if last_DC_value != current_DC_value:
        PlotTemps(time_values, temperature_values, start_DC, last_DC_value)
        start_time = full_time_values[i]
        start_DC = last_DC_value

        time_values = [full_time_values[i] - start_time]
        temperature_values = [full_temperature_values[i]]
    else:
        time_values.append(full_time_values[i] - start_time)
        temperature_values.append(full_temperature_values[i])
PlotTemps(time_values, temperature_values, start_DC, last_DC_value)