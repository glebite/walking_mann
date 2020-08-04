#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import logging

logging.basicConfig(level=logging.DEBUG)


class Display:
    """
    """
    def __init__(self):
        """
        """
        logging.debug('initializing...')
        self.RST = 24
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

        logging.debug('creating/connecting MQTT system')
        self.client = mqtt.Client("display")
        self.client.connect("127.0.0.1", port=1883, keepalive=60)
        self.client.subscribe("display")
        self.client.on_message = self.on_message

        logging.debug('setting up display')
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
        self.font = ImageFont.load_default()
        
        
    def loop(self):
        """
        """
        logging.debug('entering loop')
        self.client.loop_start()
        while True:
            time.sleep(0.1)

    
    def on_message(self, client, userdata, message):
        """
        """
        clean_msg = str(message.payload.decode('utf-8')).split(' ')
        logging.debug('clean message is: {}'.format(clean_msg))
        command = clean_msg[0]
        if command == "camera":
            logging.debug("Handling camera")
            display.clear()
            image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')
            display.image(image)
            display.display()
            image = Image.new('1', (128, 64))
        elif command == "time":
            logging.debug("Handling time...")
            display.clear()
            image = Image.new('1', (128, 64))
            draw.text((0,0),clean_msg[1],font=font, fill=255)
            display.image(image)
            display.display()
    
# display = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# font = ImageFont.load_default()
# image = Image.new('1', (128, 64))
# draw = ImageDraw.Draw(image)

# display.begin()
# display.clear()
# display.display()


if __name__=="__main__":
    DISPLAY = Display()
    DISPLAY.loop()
