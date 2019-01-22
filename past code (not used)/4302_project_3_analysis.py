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

file_name = '_4203_project_31542608156.4646575'
data = pd.read_csv(file_name + '.csv')
data = data.reset_index(drop=True) # reset the index
data = data.reset_index()
data.columns

def model(t, tau, K, C):
    return K*(1 - np.exp(np.divide(np.negative(t), tau))) + C

def model_down(t, tau, K, C):
    return K*(np.exp(np.divide(np.negative(t), tau))) + C

# def record_model_params(popt, start_DC, end_DC):
#     try:
#         with open('_4203_project_3_model_params.csv', 'a', newline='') as csvfile:
#             temperaturewriter = csv.writer(csvfile, delimiter=',')
#          #   temperaturewriter.writerow(['start_DC', 'end_DC', 'tau', 'Kp', 'C'])
#             temperaturewriter.writerow([start_DC, end_DC, popt[0], popt[1], popt[2]])  
#     except:
#         print("weird file error", time.time())

def PlotTemps(time_values, temperature_values, start_DC, end_DC):
    if start_DC == end_DC:
        return
    # step = []
    # for i in range(len(time_values)-1):
    #     step.append(time_values[i+1] - time_values[i])

    # adjusted_temperature_values1 = temperature_values[:-1]-np.min(temperature_values)#)/(np.max(temperature_values) - np.min(temperature_values))
    # adjusted_temperature_values2 = temperature_values[1:]-np.min(temperature_values)#)/(np.max(temperature_values) - np.min(temperature_values))
    # U = np.matrix([adjusted_temperature_values1, step]).T
    # z = np.matrix([adjusted_temperature_values2]).T
    # a_b = ((U.T*U).I)*(U.T)*z
    # a = a_b[0].item()
    # b = a_b[1].item()  #.item() takes a 1 x 1 matrix and makes it a scalar 
    # tau = -3/np.log(a)
    # Kp = b/(1-a)
    # print('a is equal to', a, 'b is equal to', b)
    # print('tau is equal to', tau, 'Kp is equal to', Kp)
    # t = np.linspace(0, np.max(time_values), num=400)
    # y_fit = [(Kp)*(1-np.exp(np.divide(np.negative(t_i), tau)))+np.min(temperature_values) for t_i in t]
    """popt is optimal value for parametrs: tau here
pcov is covariance of popt...how well it did"""
    popt, pcov = curve_fit(model_down, time_values, temperature_values, p0=(166, -13, 37))

    record_model_params(popt, start_DC, end_DC)

    plt.figure(figsize=(figwidth,figheight))
    plt.plot(time_values,temperature_values,color='m',label='DC ' + str(start_DC) + ' to ' + str(end_DC)) # plot temp against time
    #plt.plot(t, y_fit, 'b-', label='statistical method' )
    plt.plot(time_values, model_down(time_values, *popt), 'g', label= r'$f(t) = $' + str(round(popt[1], 2)) + r'$exp(-t/$' + str(round(popt[0], 2)) + r'$) + $' + str(round(popt[2], 2)))
    plt.legend()
    plt.ylabel('Temperature (' + r'$\degree$' +'C)',fontsize=fs)
    plt.xlabel('Time (s)',fontsize=fs)
    plt.savefig('oz_testTemperature'+ str(start_DC) +'to' + str(end_DC) + '.svg')
    #plt.show()

full_time_values = data['Time']
full_temperature_values = data['Temp']
full_dc_values = data['DC']

time_values = [0]
temperature_values = [25]
start_time = 0

start_DC = 0
for i in range(1, len(data['Time'])):
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