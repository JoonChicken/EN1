import machine
from machine import Pin, I2C
from time import sleep
import network
from umqttsimple import MQTTClient
from s2pico_oled import OLED

# DHT11 support is built in to MicroPython, just import the library:
from dht import DHT11

# Set up the sensor
# We're using pin 23, but any digital pin will work
inside = DHT11(Pin(38))

wlan = network.WLAN(network.STA_IF)


# OLED stuff:
i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = OLED(i2c, Pin(18))


# If the network isn't already connected, try to connect
if not wlan.isconnected():
    wlan.active(True)

    # Try to connect to Tufts_Wireless:
    ssid = "Tufts_Wireless"
    print("Connecting to {}...".format(ssid))
    oled.text("Connecting to", 0, 0)
    oled.text(ssid, 0, 12)
    oled.show()
    wlan.connect(ssid)
    while not wlan.isconnected():
        sleep(1)
        print('.')

print("Connected!")
print("IP address:", wlan.ifconfig()[0])
oled.fill(0)
oled.text("Connected! IP:", 0, 0)
oled.text(str(wlan.ifconfig()[0]), 0, 12)
oled.show()

# Note that this server is only accessible from the Tufts network
mqtt_server = "bell-iot.eecs.tufts.edu"

# Some kind of unique identifier, esp32-[YOUR UTLN] is good
# for example - esp32-ecarlson
clientId = "esp32-jheo"

client = MQTTClient(clientId, mqtt_server)
client.connect()
client.publish(clientId + "/ip", wlan.ifconfig()[0])


sleep(3)
oled.fill(0)
oled.show()
sleep(1)
oled.text("Ready for data", 0, 0)
oled.text("collection", 0, 12)
oled.show()
sleep(3)
oled.fill(0)


while True:
    try:
        if not wlan.isconnected():
            wlan.active(True)

            # Try to connect to Tufts_Wireless:
            ssid = "Tufts_Wireless"
            print("Connecting to {}...".format(ssid))
            oled.text("Connecting to", 0, 0)
            oled.text(ssid, 0, 12)
            oled.show()
            wlan.connect(ssid)
            while not wlan.isconnected():
                sleep(1)
                print('.')
        
        
        client = MQTTClient(clientId, mqtt_server)
        client.connect()
        client.publish(clientId + "/ip", wlan.ifconfig()[0])
                
                
        # Take a measurement from the sensor
        oled.text("measuring...", 0, 0)
        oled.show()
        inside.measure()
        
        oled.fill(0)
        oled.show()
        
        # After we've taken a measurement, we can call the temperature() function
        # to retrieve the actual temperature
        oled.text("separating...", 0, 0)
        oled.show()
        degC = inside.temperature()
        humidity = inside.humidity()
        
        oled.fill(0)
        oled.show()
        
        # Convert Celcius to Farenheit
        oled.text("converting...", 0, 0)
        oled.show()
        degF = degC * 9.0 / 5.0 + 32
        print(f"inside {degF} F  {humidity}% RH")
        
        oled.fill(0)
        oled.show()
        
        oled.text("publishing...", 0, 0)
        oled.show()
        client.publish(clientId + "/data_final", str(degF) + "," + str(humidity))
        
        oled.fill(0)
        oled.show()
        
        for i in range(5):
            oled.text("Recording to", 0, 0)
            oled.text(clientId, 0, 12)
            oled.text(str(degF) + "F " + str(humidity) + "%", 0, 24)
            oled.show()
            sleep(3)
            oled.fill(0)
            oled.show()
            sleep(3)
        
    except:
        print("Error getting data. Trying again...")
        degF = humidity = 0
        
        oled.text("ERROR", 0, 12)
        oled.show()
        sleep(2)
        oled.fill(0)
        oled.show()
    finally:
        sleep(0.5)













