from umqttsimple import MQTTClient
from machine import Pin, I2C
from time import sleep
from ahtx0 import AHT20


i2c = I2C(1, sda=Pin(3), scl=Pin(1))

sensor = AHT20(i2c)
sensor.reset()
print(sensor.initialize())


while True:
    degC = sensor.temperature
    humidity = sensor.relative_humidity
    print("\nTemperature: %0.2f C" % degF)
    print("Humidity: %0.2f %%" % humidity)
    time.sleep(0.2)

# Note that this server is only accessible from the Tufts network
mqtt_server = "bell-iot.eecs.tufts.edu"
# Some kind of unique identifier, esp32-[YOUR UTLN] is good
clientId = "ESP32-jheo"
client = MQTTClient(clientId, mqtt_server)
client.connect()
client.publish(clientId + "/ip", wlan.ifconfig()[0])