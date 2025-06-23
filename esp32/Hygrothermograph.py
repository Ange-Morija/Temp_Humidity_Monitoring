from time import sleep_ms
from machine import I2C, Pin
from I2C_LCD import I2cLcd
import dht, utime, network, urequests

SSID     = 'Freebox-602F24' # Enter your WiFi SSID
PASSWORD = 'v5kfkqzbr3qs236vqh2sx9' # Enter your WiFi password

# Set your room and sensor_id
room = "livingroom"
sensor_id = "esp32_01"

# InfluxDB Cloud Info
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/write?org=geodemy&bucket=living_room&precision=s"
INFLUX_TOKEN = "cm5T3qYHR1GEY_62e24bTA1Agoi2xgljtBn_gfNK7fZx0ZX2uq-Ukkchx1eFot9LlYmgXT19O7sgjmKOFf87MA=="
headers = {
    "Authorization": "Token " + INFLUX_TOKEN,
    "Content-Type": "text/plain"
}

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        lcd.move_to(0, 0)
        lcd.putstr("connecting...")
        wlan.connect(SSID, PASSWORD) 
    start = utime.time()
    while not wlan.isconnected():
        utime.sleep(1)
        if utime.time() - start > 10:
            print("connect timeout!")
            lcd.move_to(0, 0)
            lcd.putstr("connect timeout!  ")
            break
    if wlan.isconnected():
        print('network config:', wlan.ifconfig())
        lcd.move_to(0, 0)
        lcd.putstr("connected")

def send_data(id_value, temp, hum):
    
    line = f"climate,room={room},sensor_id={sensor_id} temperature={temp},humidity={hum},value_id={id_value}"
    try:
        response = urequests.post(INFLUX_URL, data=line, headers=headers)
        if response.status_code == 204:
            pass
        else:
            print("Failed to send data:", response.status_code, response.text)
        response.close()
    except Exception as e:
        print("Error sending data:", e)


led = Pin(2, Pin.OUT) # create LED object from pin2, set Pin2 to output

DHT = dht.DHT11(Pin(18))
i2c = I2C(scl=Pin(14), sda=Pin(13), freq=400000)
devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device!")
else:
    for device in devices:
        print("I2C addr:", hex(device))
        lcd = I2cLcd(i2c, device, 2, 16)

wifi_connect()
sleep_ms(2000)
lcd.move_to(0, 0)
lcd.putstr("Reading data...")
sleep_ms(2000)
lcd.move_to(0, 0)
lcd.putstr(" " * 16)
sleep_ms(1000)

id_value = 1

try:
    while True:
        led.value(1)        # Turn LED on        
        DHT.measure()
        temp = DHT.temperature()
        hum = DHT.humidity()
        
        lcd.move_to(0, 0)
        lcd.putstr("Temperature: " + str(temp) + " °C   ")
        lcd.move_to(0, 1)
        lcd.putstr("Humidity: " + str(hum) + " % ")
        
        sleep_ms(1000)
        
        # Sending the data to InfluxDB
        send_data(id_value, temp, hum)
        id_value = id_value + 1
        
        led.value(0)        # Turn LED off
        sleep_ms(1000)      # Wait ~2 seconds in total
except Exception as e:
    print("Exception in main loop:", e)

