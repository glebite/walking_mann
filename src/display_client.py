#!/usr/bin/env python3
"""
display_client.py - uses mqtt for messaging and relaying info to the 
                    display
"""

import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import logging

LOGGER = logging.getLOGGER('display_client')
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler('display_client.log')
FH.setLevel(logging.DEBUG)
FORMATTER = logging.FORMATTER('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FH.setFORMATTER(FORMATTER)
LOGGER.addHandler(FH)

class Display:
    """
    Display
    """
    def __init__(self):
        """
        __init__
        """
        LOGGER.debug('initializing...')
        self.RESET = 24
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

        LOGGER.debug('creating/connecting MQTT system')
        self.client = mqtt.Client("display")
        self.client.connect("127.0.0.1", port=1883, keepalive=60)
        self.client.subscribe("display")
        self.client.on_message = self.on_message

        LOGGER.debug('setting up display')
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=self.RESET)
        self.font = ImageFont.truetype('/home/pi/VCR_OSD_MONO_1.001.ttf', 48)
        self.display.begin()
        
    def loop(self):
        """
        loop
        """
        LOGGER.debug('entering loop')
        self.client.loop_start()
        while True:
            time.sleep(0.1)

    
    def on_message(self, client, userdata, message):
        """
        on_message
        """
        clean_msg = str(message.payload.decode('utf-8')).split(' ')
        LOGGER.debug('clean message is: {}'.format(clean_msg))
        command = clean_msg[0]
        if command == "camera":
            LOGGER.debug("Handling camera")
            return_code = self.display.clear()
            LOGGER.debug('display.clear rc: {}'.format(return_code))
            return_code = self.display.display()
            LOGGER.debug('display.display rc: {}'.format(return_code))
            image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')
            LOGGER.debug('image creation from local icons folder: {}'.format(image))
            return_code = self.display.image(image)
            LOGGER.debug('display.image rc: {}'.format(return_code))
            return_code = self.display.display()
            LOGGER.debug('display.display rc: {}'.format(return_code))
        elif command == "time":
            LOGGER.debug("Handling time...")
            return_code = self.display.clear()
            LOGGER.debug('display.clear rc: {}'.format(return_code))
            return_code = self.display.display()
            LOGGER.debug('display.clear rc: {}'.format(return_code))          

            im = Image.new('1',(128,64))
            LOGGER.debug('image creation: {}'.format(im))
            draw = ImageDraw.Draw(im)
            return_code = draw.text((0,0), clean_msg[1], font=self.font, fill=255)
            LOGGER.debug('draw results: {}'.format(return_code))
            return_code = self.display.image(im)
            LOGGER.debug('display.image rc: {}'.format(return_code))
            return_code = self.display.display()
            LOGGER.debug('display.display rc: {}'.format(return_code))
        elif command == "clear":
            return_code = self.display.clear()
            LOGGER.debug('display.clear rc: {}'.format(return_code))
            return_code = self.display.display()
            LOGGER.debug('display.display rc: {}'.format(return_code))

if __name__ == "__main__":
    DISPLAY = Display()
    DISPLAY.loop()
