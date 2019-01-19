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

file_name = 'paper'
data = pd.read_csv(file_name + '.csv')
data = data.reset_index(drop=True) # reset the index
data = data.reset_index()
data.columns


full_time_values = data['time']
full_temperature_values = data['temperature']
#full_dc_values = data['DC']
fig, host = plt.subplots()

par1 = host.twinx()

p1, = host.plot(full_time_values, full_temperature_values, "r--", label='Temperature (' + r'$\degree$' +'C)')
#p2, = par1.plot(full_time_values, full_dc_values, "b--")

host.set_xlim(0, 820)
host.set_ylim(24, 35)
#par1.set_ylim(-.5, 1.5)
# host.set_xlim(0, 1200)
# host.set_ylim(20, 35)
# par1.set_ylim(-0.4, 1)
host.set_xlabel("Time (s)", fontsize=fs)
host.set_ylabel('Temperature (' + r'$\degree$' +'C)',fontsize=fs)
#par1.set_ylabel("DC", fontsize=fs, labelpad =.0001)
p3, = host.plot([15, 820], [33,33], label = 'SP = 33'+ r'$\degree$' + 'C', color = 'black', zorder = 3)
host.plot([15,15],[25, 33], color ='black')
#p4, = host.plot([2400, 4800], [36,36], label = 'SP = 36'+ r'$\degree$' + 'C', color = 'm', zorder = 3)
#host.plot([2400,2400],[33, 36], color ='m')
# par1.set_ylabel("DC", fontsize=fs, labelpad = .3)
# p3, = host.plot([np.min(full_time_values), 1200], [33,33], label = 'SP = 33'+ r'$\degree$' + 'C', color = 'black', zorder = 3)
# host.plot([np.min(full_time_values),np.min(full_time_values)],[25, 33], color ='black')
# # p4, = host.plot([1200, 2400], [36,36], label = 'SP = 36'+ r'$\degree$' + 'C', color = 'm', zorder = 3)
# # host.plot([1200,1200],[33, 36], color ='m')

host.yaxis.label.set_color(p1.get_color())
#par1.yaxis.label.set_color(p2.get_color())
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
#par1.tick_params(axis='y', colors=p2.get_color(), **tkw)

host.tick_params(axis='x', **tkw)

lines = [p1, p3]# p4]

host.legend(lines, [l.get_label() for l in lines], loc = 4, fontsize = 12)
plt.savefig('4203_paper1.svg')
plt.show()


        