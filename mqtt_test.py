import network
from umqttsimple import MQTTClient
from time import sleep

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

# Identify ourselves
client.publish(clientId + '/ip', wlan.ifconfig()[0])
client.publish(clientId + '/test', "Hello World!")