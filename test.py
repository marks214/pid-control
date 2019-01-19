# We want to collect experimental data
# describing the response of the measured T to the changes
# in the control input
# change the duty cycle (DC) of the PWM
# 

import matplotlib.pyplot as plt
import matplotlib.animation as animation #Required to live plot
import numpy as np
import csv
import time #Required to timestamp & delay functions
from pylive import live_plotter
import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
from progress.bar import ChargingBar #required to display a charging bar


portName = 'COM3'
arduino = pyfirmata.Arduino(portName)
it = pyfirmata.util.Iterator(arduino)
it.start()

#Connect to arduino hardware on input port.
input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
output_pin = arduino.get_pin('d:3:o') #digital, output from the computer
output_pin.mode = 3  #PWM mode

# Set digital pin 3 to high to heat up resistor R2
output_pin.write(1)
time.sleep(10)
signal0 = input_pin.read()
print(signal0, 'signal0')

bar = ChargingBar('Heating up...', max=20)
signal1 = 0
for i in range(20):
    time.sleep(5)
    bar.next()
bar.finish()
       
# Read the voltage to analog pin 0 after R2 has heated
signal1 = input_pin.read()
print(signal1, 'signal1')
print((signal0 - signal1),' V.')
# Set the output of digital pin 3 to low (0V)
output_pin.write(0)
R_25 = np.log((signal1/signal0)*((5-signal0)/(5-signal1)))
T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*R_25 + 2.620131e-06*R_25**2 + 6.383091e-08*R_25**3 ))
T_Celcius = (T_Kelvin)-273.15
print(R_25, T_Kelvin, T_Celcius)

""" test
signal1 = .346
signal0 = .4233
R_25 = np.log((signal1/signal0)*((5-signal0)/(5-signal1)))
T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*R_25 + 2.620131e-06*R_25**2 + 6.383091e-08*R_25**3 ))
T_Celcius = (T_Kelvin)-273.15
print(R_25, T_Kelvin, T_Celcius)
"""

start_time = time.time()
DC_max = 1
DC_step = 0.1
seconds_between_readings = 1
readings_per_step = 1

DC_values = []
temperature_values = []

def update_duty_cycle(DC): #DC = duty cycle
    # send signal to arduino
    return

def get_temperature():
    # read from arduino and do calculation
    return np.random.randn(1)[0]

def wait_for_temperature_to_equalize(DC):
    for i in range(readings_per_step):
        temperature = get_temperature()
        record_temperature(temperature, DC)

        DC_values.append(time.time())
        temperature_values.append(temperature)

        time.sleep(seconds_between_readings)
    return

#def time_stamp():
 #   now = str(start_time)
  #  return now

def record_temperature(temperature, DC):
    with open('4203_project_3' + str(start_time) + '.csv', 'a', newline='') as csvfile:
        temperaturewriter = csv.writer(csvfile, delimiter=',')
        temperaturewriter.writerow([time.time(), temperature, DC])     
    return

def run():
    DC = 0
    line1 = []
    while DC <= DC_max:
        update_duty_cycle(DC)
        wait_for_temperature_to_equalize(DC)
        #line1 = live_plotter(DC_values,temperature_values,line1)
        DC += DC_step
    line1 = live_plotter(DC_values,temperature_values,line1)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

"""def animate(i):
    pullData = open('4203_project_3.csv',"r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
"""       
# https://github.com/engineersportal/pylive/blob/master/LICENSE
# the function below is for updating both x and y values (great for updating dates on the x-axis)
def start_plot():
    plt.ion()
    fig = plt.figure(figsize=(13,6))
    ax = fig.add_subplot(111)
    line1, = ax.plot(x_vec,y1_data,'r-o',alpha=0.8)
    plt.ylabel('Y Label')
    plt.title('Title: {}'.format(identifier))
    plt.show()

def live_plotter_xy(x_vec,y1_data,line1,identifier='',pause_time=0.01):

        
    line1.set_data(x_vec,y1_data)
    plt.xlim(np.min(x_vec),np.max(x_vec))
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])

    plt.pause(pause_time)
    
    return line1
run() 
wait = input("Press Enter to Continue")
