import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

file = open("data.csv", 'r')
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


# plotting
plt.plot(timestamp, temperature)
plt.plot(timestamp, humidity)
plt.xlabel("Time")
plt.ylabel("Temperature (ºC) / Humidity(%)")
plt.title("Temperature and Humidity over time")
plt.show()