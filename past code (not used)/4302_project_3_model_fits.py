import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
from datetime import datetime, date
import numpy as np
from datetime import datetime

figwidth = 10
figheight = 8
fs = 15

def linear_model(x, m, b):
    return np.add(np.multiply(m, x), b)

def exponential_model(x, m, b, r):
    return np.add(np.multiply(m, np.exp(np.multiply(r,x))), b)

def PlotLinear(x, y, term):
    
    popt, pcov = curve_fit(linear_model, x, y)
    plt.figure(figsize=(figwidth,figheight))
    plt.scatter(x,y,color='m',label=term) # plot temp against time
    #plt.plot(t, y_fit, 'b-', label='statistical method' )

    plt.plot(x, linear_model(x, *popt), 'g-', label= 'y(DC) = '+ str(round(popt[0], 2)) + '(DC) + ' + str(round(popt[1], 2)))
    plt.legend()
    plt.ylabel(term,fontsize=fs)
    plt.xlabel('DC',fontsize=fs)
    plt.savefig('linear' + term + '.svg')
    #plt.show()

def PlotExponential(x, y, term):
    
    popt, pcov = curve_fit(exponential_model, x, y, p0=(480,210,-13))
    plt.figure(figsize=(figwidth,figheight))
    plt.scatter(x,y,color='m',label=term) # plot temp against time
    #plt.plot(t, y_fit, 'b-', label='statistical method' )

    plt.plot(x, exponential_model(x, *popt), 'g-', label= 'y(DC) = '+ str(round(popt[0], 2)) + 'exp(' + str(round(popt[2], 2)) + '(DC)) + ' + str(round(popt[1], 2)))
    plt.legend()
    plt.ylabel(term,fontsize=fs)
    plt.xlabel('DC',fontsize=fs)
    plt.savefig('exp' + term + '.svg')

#def calculate(x, y, term):
    
 #   popt, pcov = curve_fit(linear_model, x, y)
  #  K_p = []
   # tau = []
    #C = []
""" 
K_p_down = []
tau_down = []
C_down = []
DC = [0.1, 0, 0.2, 0, 0.3, 0, 0.4, 0, 0.5, 0, 0.6, 0, 0.7, 0, 0.8, 0, 0.9, 0, 1, 0, 0.15, 0, 0.25, 0, 0.35, 0]

for i in range(len(DC)):
    if (i % 2) == 0:
        K_p.append(int(popt[0]))
        tau.append(int(popt[1]))
        C.append(int(popt[2]))
    else:
        K_p_down.append(int(popt[0]))
        tau_down.append(int(popt[1]))
        C_down.append(int(popt[2]))    """

K_p = [1.33, 3.83, 4.33, 5.56, 7.30, 8.92, 10.46, 11.61, 12.36, 13.02, 14.29, 15.22]
tau = [308.64, 181.7, 224.93, 205.8, 180.09, 173.06, 173.98, 186.12, 191.89, 166.26, 183.13, 162.67]
C = [26.57, 28.06747348, 27.29, 29.6961958, 31.11876663, 32.60041819, 34.00172712, 35.40278965, 35.77, 36.60390916, 38.1, 39.0]


K_p_down = [-2.35, -4.09, -4.85, -5.79, -7.61, -9.16, -10.66, -11.48, -13.34, -13.75, -13.71, -16.35]
#tau_down = [238.96, 231.43, 210.18, 225.19, 221.15, 212.50, 216.11, 218.79, 195.91, 204.63, 222.15, 203.48]
C_down = [24.10168751, 23.81565614, 22.48, 23.60659569, 23.44312709, 23.39079975, 23.27244527, 23.16981517, 23.89, 23.15681687, 23.07075782, 23.13]
DC = [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1]
print(len(K_p_down))
"""file_name = '_4203_project_3_model_params'
data = pd.read_csv(file_name + '.csv')
data = data.reset_index(drop=True) # reset the index
data = data.reset_index()
data.columns

DC = data['end_DC']
K_p = data['Kp']
tau = data['tau']
C = data['C']"""

DCspecial = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
tau_down = [238.96, 231.43, 225.19, 221.15, 212.50, 216.11, 218.79, 204.63, 222.15, 203.48]

PlotLinear(DC, K_p, 'Kp heating')
PlotExponential(DC, tau, 'tau heating')
PlotLinear(DC, C, 'C heating')

PlotLinear(DC, K_p_down, 'Kp cooling')
PlotExponential(DCspecial, tau_down, 'tau cooling')
PlotLinear(DC, C_down, 'C cooling')


