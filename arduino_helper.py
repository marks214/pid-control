import time  # Required to timestamp & delay functions
from random import shuffle
import numpy as np
import pyfirmata  # facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
from progress.bar import ChargingBar  # required to display a charging bar

class  ArduinoHelper(object):
    portName = 'COM3'

    def __init__(self):
        self.arduino = pyfirmata.Arduino(self.portName)
        it = pyfirmata.util.Iterator(self.arduino)
        it.start()
        self.start_time = time.time()
        self.input_pin = self.arduino.get_pin('a:0:i') #analog, input to the computer
        self.output_pin = self.arduino.get_pin('d:6:p') #digital, PWM mode, from the computer

        # make sure the PWM pin (6) is off, wait a number of seconds
        # (gives enough time so everything is ready to be read - otherwise it may read "None")
        time.sleep(2)
        self.update_duty_cycle(0)

    def read_input_pin(self):
        return self.read_voltage(self.input_pin)

    def read_voltage(self, pin):
        """
            Returns the voltage of the pin passed in (between 0 and 5 Volts)
            It takes a number of measurements, then averages them to reduce noise
        """
        outputs = []
        for i in range(10):
            time.sleep(.1)
            outputs.append(pin.read())
        return 5.0 * np.average(outputs)

    def update_duty_cycle(self, DC): 
        self.output_pin.write(DC)