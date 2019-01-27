from arduino_helper import ArduinoHelper
import time

board = ArduinoHelper()

while True:
    is_switch_on = board.is_switch_on()
    board.write_to_lcd(is_switch_on)