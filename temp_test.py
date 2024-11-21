from machine import Pin, I2C
from time import sleep
from ahtx0 import AHT20

# Set up the temperature sensor
# does not need to be pin 38 and 37
i2c = I2C(1, sda=Pin(3), scl=Pin(1))
therm = AHT20(i2c)

# take a measurement
degC = therm.temperature
humidity = therm.relative_humidity

# Convert Celcius to Farenheit
degF = degC * 9.0 / 5.0 + 32
print(f"inside {degF} F {humidity}% RH")