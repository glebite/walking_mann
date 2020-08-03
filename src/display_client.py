import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
import time

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

def on_message(client, userdata, message):
    clean_msg = str(message.payload.decode('utf-8')).split(' ')
    command = clean_msg[0]
    if command is "camera":
        display.clear()
        display.image()
    elif command is "time":
        display.clear()
        display.text(
    
        

display = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

display.begin()
display.clear()
display.display()

client = mqtt.Client("display")
client.connect('127.0.0.1',port=1883,keepalive=60)
client.subscribe('display')

image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')

display.image(image)
display.display()

client.on_message=on_message

client.loop_start()
while True:
    time.sleep(0.1)
