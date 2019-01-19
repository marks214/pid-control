import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
import time #Required to use delay functions
from progress.bar import ChargingBar
import numpy as np

#for blue Aruino UNO use COM3, for redBoard (Sparkfun Arduni0) use COM4
portName = 'COM3'

arduino = pyfirmata.Arduino(portName)
it = pyfirmata.util.Iterator(arduino)
it.start()

#Connect to arduino hardware on input port.
input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
output_pin = arduino.get_pin('d:6:p') #digital, PWM output from the computer

# Set digital pin 6 to high to heat up 220 ohm resistor
output_pin.write(1)
time.sleep(15)
signal0 = input_pin.read()
print(signal0, 'signal0')

bar = ChargingBar('Heating up...', max=20)
for i in range(20):
    time.sleep(50)
    bar.next()
bar.finish()
       
# Read the voltage to analog pin 0 after R2 has heated
signal1 = input_pin.read()
print(signal1, 'signal1')
print(str(signal1 - signal0) + " " + '\u0394' + 'V') #unicode for Delta
# Set the output of digital pin 6 to low (0V)
output_pin.write(0)
R_ratio = np.log((signal0/signal1)*((5-5*signal1)/(5-5*signal0)))
T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*R_ratio + 2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3 ))
T_Celcius = (T_Kelvin)-273.15
print(R_ratio, T_Kelvin, T_Celcius)

arduino.exit()