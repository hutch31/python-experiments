__author__ = 'guy'

# Create performance charts for POH
import matplotlib.pyplot as plt
import matplotlib.mlab
import numpy as np
import math

def extended_values():
    ev = [(125, 0), (120, -1), (115, -2), (110, -2.5), (100, -3), (90, -2.5), (85, -2), (80, -1.6), (70, -1)]
    return np.array(ev)

def retract_values():
    rv = [(220, -2), (200, -1.6), (190, -1.3), (185, -1), (170, 0), (155, 1), (150, 1.3), (140, 1.5),
          (125, 1.5), (120, 1.5), (110, 1.5), (100, 1.3), (95, 1), (85, 0.5), (80, 0), (75, -0.5)]
    return np.array(rv)

def airspeed_correction_chart(filename=''):
    plt.figure(4, figsize=(6,8))
    ev = extended_values()
    rv = retract_values()
    plt.plot(ev[:,1], ev[:,0], label='Flaps Extended')
    plt.plot(rv[:,1], rv[:,0], label='Flaps Retracted')
    plt.grid(b=True, linestyle='-')
    plt.xlabel("Correction factor (MPH)")
    plt.ylabel("Indicated Speed (MPH)")
    plt.xlim([-5,5])
    plt.legend()
    if filename != '':
        plt.savefig(filename)
    else:
        plt.show()

def xwind_plot(maximum=40, filename=''):
    plt.figure(3, figsize=(6,7.5))
    # Draw segments for each 10 degree arc of crosswind
    for a in range(0,18):
        angle = (math.pi / 18) * a
        x = [np.sin(angle)*5, np.sin(angle)*maximum]
        y = [np.cos(angle)*5, np.cos(angle)*maximum]
        plt.plot(x, y, color='black')
    # Draw speed rings for each 10kts of wind
    for r in range(10,maximum+10,10):
        pl = matplotlib.mlab.frange(0, math.pi, math.pi/30)
        plt.plot(np.sin(pl)*r, np.cos(pl)*r, color='black')
    plt.ylabel("Headwind component")
    plt.xlabel("Crosswind component")
    plt.xlim([0, maximum])
    plt.ylim([-maximum/2,maximum])
    plt.grid(b=True, linestyle='-')
    plt.grid(b=True, which='minor', linestyle='--')
    if filename != '':
        plt.savefig(filename)
    else:
        plt.show()

def density_altitude(filename=''):
    fig = plt.figure(3, figsize=(6,8))
    # plot the ISA line
    y = np.array(range(0, 22001, 2000))
    x = 15 - 1.98*(y/1000)
    plt.plot(x, y, color='black')
    for alt in range(0, 22001, 2000):
        x = np.array(range(-40,45,5))
        y = alt+118.8*(x-(15-1.98*(alt/1000)))
        plt.plot(x, y, color='black', label=alt)
        plt.text(25-1.98*(alt/1000), alt, "{} ft".format(alt), rotation=35)
    plt.grid(b=True)
    plt.ylim([0,22000])
    plt.xlim([-40,40])
    plt.xlabel("Outside Air Temperature (C)")
    plt.ylabel("Pressure Altitude (feet)")
    if filename != '':
        plt.savefig(filename)
    else:
        plt.show()

airspeed_correction_chart('airspeed_correction.png')
xwind_plot(40, 'xwind_plot.png')
density_altitude('density_altitude.png')