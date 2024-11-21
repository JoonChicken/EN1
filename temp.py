from machine import Pin
from time import sleep
import network
from umqttsimple import MQTTClient

# DHT11 support is built in to MicroPython, just import the library:
from dht import DHT11

# Set up the sensor
# We're using pin 23, but any digital pin will work
inside = DHT11(Pin(38))

wlan = network.WLAN(network.STA_IF)

# If the network isn't already connected, try to connect
if not wlan.isconnected():
    wlan.active(True)

    # Try to connect to Tufts_Wireless:
    ssid = "Tufts_Wireless"
    print("Connecting to {}...".format(ssid))
    wlan.connect(ssid)
    while not wlan.isconnected():
        sleep(1)
        print('.')

print("Connected!")
print("IP address:", wlan.ifconfig()[0])

# Note that this server is only accessible from the Tufts network
mqtt_server = "bell-iot.eecs.tufts.edu"

# Some kind of unique identifier, esp32-[YOUR UTLN] is good
# for example - esp32-ecarlson
clientId = "esp32-jheo"

client = MQTTClient(clientId, mqtt_server)
client.connect()
client.publish(clientId + "/ip", wlan.ifconfig()[0])

while True:
    try:
        # Take a measurement from the sensor
        inside.measure()
        # After we've taken a measurement, we can call the temperature() function
        # to retrieve the actual temperature
        degC = inside.temperature()
        humidity = inside.humidity()

        # Convert Celcius to Farenheit
        degF = degC * 9.0 / 5.0 + 32
        print(f"inside {degF} F  {humidity}% RH")
        client.publish(clientId + "/data", str(degC) + "," + str(humidity))
        
    except:
        sleep(0.1)    
    finally:
        sleep(5)



