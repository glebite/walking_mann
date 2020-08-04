#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import logging

class Display:
    """
    """
    def __init__(self):
        """
        """
        self.RST = 24
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        

def on_message(client, userdata, message):
    """
    """
    global display
    global draw
    global font
    global image
    clean_msg = str(message.payload.decode('utf-8')).split(' ')
    print(clean_msg)
    command = clean_msg[0]
    if command == "camera":
        print("Handling camera")
        display.clear()
        image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')
        display.image(image)
        display.display()
        image = Image.new('1', (128, 64))
    elif command == "time":
        print("Handling time...")
        display.clear()
        image = Image.new('1', (128, 64))
        draw.text((0,0),clean_msg[1],font=font, fill=255)
        display.image(image)
        display.display()
    
display = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
font = ImageFont.load_default()
image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

display.begin()
display.clear()
display.display()

client = mqtt.Client("display")
client.connect('127.0.0.1',port=1883,keepalive=60)
client.subscribe('display')

client.on_message=on_message

client.loop_start()
while True:
    time.sleep(0.1)

if __name__=="__main__":
    DISPLAY = Display()
    DISPLAY.loop()
