import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
import numpy as np
from time import sleep


try:
    portName = 'COM3' #assigns a variable
    arduino = pyfirmata.Arduino(portName) #creates an instance of a class
    it = pyfirmata.util.Iterator(arduino)
    it.start() #calls a start method

    #Connect to arduino hardware on input port.
    input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
    sleep(1)

    Vout = input_pin.read()
    print(Vout*5, 'Vout')
    
finally:
    arduino.exit()
