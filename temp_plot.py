import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
from mpl_toolkits.axes_grid1 import host_subplot


file = open("data_final1.csv", 'r')           # change to reflect your file
data = csv.reader(file)
discard = next(data)

# reading data into array
timestamp = []
temperature = []
humidity = []
for row in data:
    timestamp.append(datetime.fromtimestamp(int(row[0])))
    temperature.append(row[1])
    humidity.append(row[2])


host = host_subplot(111)
par = host.twinx()

host.set_xlabel("Time")
host.set_ylabel("Temperature")
par.set_ylabel("Humidity")

p1, = host.plot(timestamp, temperature, label="Temperature")
p2, = par.plot(timestamp, humidity, label="Humidity")

plt.show()

"""
plt.plot(timestamp, temperature)
plt.plot(timestamp, humidity)
plt.xlabel("Time")
plt.ylabel("Temperature (ºF) / Humidity(%)")
plt.title("Temperature and Humidity over time")
plt.show()
"""