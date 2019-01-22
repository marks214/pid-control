'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
DC = np.arange(0, 1, 0.01)
Y = np.arange(0, 1200, 1)
DC, Y = np.meshgrid(DC, Y)
Z = -(-15.16*DC - 1.21)*np.exp(-Y/(41.78*np.exp(-3.12*DC)+208.55))-0.51*DC+23.65

# Plot the surface.
surf = ax.plot_surface(DC, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z and y axis.
ax.set_zlim(22, 42)
ax.zaxis.set_major_locator(LinearLocator(5))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#ax.yaxis.set_major_locator(LinearLocator(6))
#ax.yaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel('DC')
ax.set_ylabel('time (s)')
ax.set_zlabel('Temperature (' + r'$\degree$' +'C)')
plt.savefig('3D_cooling.svg')
