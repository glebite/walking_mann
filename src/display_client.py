#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import logging

logger = logging.getLogger('display_client')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('display_client.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class Display:
    """
    """
    def __init__(self):
        """
        """
        logger.debug('initializing...')
        self.RST = 24
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

        logger.debug('creating/connecting MQTT system')
        self.client = mqtt.Client("display")
        self.client.connect("127.0.0.1", port=1883, keepalive=60)
        self.client.subscribe("display")
        self.client.on_message = self.on_message

        logger.debug('setting up display')
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
        self.font = ImageFont.truetype('/home/pi/VCR_OSD_MONO_1.001.ttf', 48)
        self.display.begin()
        
    def loop(self):
        """
        """
        logger.debug('entering loop')
        self.client.loop_start()
        while True:
            time.sleep(0.1)

    
    def on_message(self, client, userdata, message):
        """
        """
        clean_msg = str(message.payload.decode('utf-8')).split(' ')
        logger.debug('clean message is: {}'.format(clean_msg))
        command = clean_msg[0]
        if command == "camera":
            logger.debug("Handling camera")
            rc = self.display.clear()
            logger.debug('display.clear rc: {}'.format(rc))
            rc = self.display.display()
            logger.debug('display.display rc: {}'.format(rc))
            image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')
            logger.debug('image creation from local icons folder: {}'.format(image))
            rc  = self.display.image(image)
            logger.debug('display.image rc: {}'.format(rc))
            rc = self.display.display()
            logger.debug('display.display rc: {}'.format(rc))
        elif command == "time":
            logger.debug("Handling time...")
            rc = self.display.clear()
            logger.debug('display.clear rc: {}'.format(rc))            
            rc = self.display.display()
            logger.debug('display.clear rc: {}'.format(rc))            
            
            im = Image.new('1',(128,64))
            logger.debug('image creation: {}'.format(im))
            draw = ImageDraw.Draw(im)
            rc = draw.text((0,0),clean_msg[1],font=self.font, fill=255)
            logger.debug('draw results: {}'.format(rc))
            rc = self.display.image(im)
            logger.debug('display.image rc: {}'.format(rc))            
            rc = self.display.display()
            logger.debug('display.display rc: {}'.format(rc))            
        elif command == "clear":
            rc = self.display.clear()
            logger.debug('display.clear rc: {}'.format(rc))            
            rc = self.display.display()
            logger.debug('display.display rc: {}'.format(rc))            
            
if __name__=="__main__":
    DISPLAY = Display()
    DISPLAY.loop()
