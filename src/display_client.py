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
        self.font = ImageFont.truetype('/home/pi/VCR_OSD_MONO_1.001.ttf', 48)
        self.display.begin()
        
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
            self.display.clear()
            self.display.display()
            image = Image.open('icons/camera_icon.ppm').resize((128,64), Image.ANTIALIAS).convert('1')
            self.display.image(image)
            self.display.display()
        elif command == "time":
            logging.debug("Handling time...")
            self.display.clear()
            self.display.display()
            im = Image.new('1',(128,64))
            draw = ImageDraw.Draw(im)
            draw.text((0,0),clean_msg[1],font=self.font, fill=255)
            self.display.image(im)
            self.display.display()
        elif command == "clear":
            self.display.clear()
            self.display.display()
            
if __name__=="__main__":
    DISPLAY = Display()
    DISPLAY.loop()
