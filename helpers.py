import time
import numpy as np
from progress.bar import ChargingBar
from threading import Thread

def calculate_temperature(signal0, signal1):
    """
       Calculates the temerature from an initial reference voltage and a current voltage (each between 0 and 5)
    """

    R_ratio = np.log((signal0/signal1)*((5-5*signal1)/(5-5*signal0)))
    T_Kelvin = 1/((0.003354016 + 0.0002569850*R_ratio +
                   2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3))
    return (T_Kelvin)-273.15


def display_loading_bar(seconds: int = 60):
   number_of_bars = 20
   message = 'Heating up...'  
   bar = ChargingBar(message, max=number_of_bars)
   for _ in range(number_of_bars):
       time.sleep(seconds / number_of_bars)
       bar.next()
   bar.finish()
