#!/usr/bin/env bash

sleep 10

h=`date +"%H"`
mosquitto_pub -t 'display' -m 'time '$h'H'
sleep 4

m=`date +"%M"`
mosquitto_pub -t 'display' -m 'time '$m'M'

sleep 4
mosquitto_pub -t 'display' -m 'clear'
