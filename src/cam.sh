#!/usr/bin/env bash
# cam.sh - capture a camera image and publish notification of the camera operating...

mosquitto_pub -h 127.0.0.1 -t display -m "camera"
raspistill -w 1024 -h 768 -q 75 -o camera-`date '+%Y-%m-%dT%H:%M:%S'`.jpg
