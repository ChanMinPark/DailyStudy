#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import *
import sys
import smbus
import time
import requests
import json
import serial,os
import RPi.GPIO as GPIO
import fcntl, socket, struct
from co2led import *

SHT20_ADDR = 0x40       # SHT20 register address
SHT20_CMD_R_T = 0xF3    # no hold Master Mode (Temperature)
SHT20_CMD_R_RH = 0xF5   # no hold Master Mode (Humidity)
SHT20_CMD_RESET = 0xFE  # soft reset

DEBUG_PRINT = 1
SERIAL_READ_BYTE = 12

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

def reading(v):
    bus.write_quick(SHT20_ADDR)
    if v == 1:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_T)
    elif v == 2:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_RH)
    else:
        return False
    time.sleep(.1)
    b = (bus.read_byte(SHT20_ADDR)<<8)
    b += bus.read_byte(SHT20_ADDR)
    return b

def calc(temp, humi):
    tmp_temp = -46.85 + 175.72 * float(temp) / pow(2,16)
    tmp_humi = -6 + 125 * float(humi) / pow(2,16)
    return tmp_temp, tmp_humi

# check length, alignment of incoming packet string
def syncfind():
    index = 0
    alignment = 0
    while 1:
        in_byte = serial_in_device.read(1)
# packet[8] should be 'm'
# end of packet is packet[10]
        if in_byte is 'm' :
            #print 'idx =', index, in_byte
            alignment = 8
        if alignment is 10 : 
            alignment = 1
            index = 0
            break
        elif alignment > 0 :
            alignment += 1
        index += 1

def checkAlignment(incoming):
    idxNum = incoming.find('m')
    # idxNum is 9, correct
    offset = idxNum - 9 
    if offset > 0 :
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    if offset < 0 :
        offset = 12 + offset 
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    return new_str


def getCO2():
    ledall_off()
    
    try:
        serial_in_device = serial.Serial('/dev/ttyAMA0',38400)
    except serial.SerialException, e:
        logger.error("Serial port open error")
        ledall_off()
    
    ppm=0
    try:
        in_byte = serial_in_device.read(SERIAL_READ_BYTE)
        pos = 0
    except serial.SerialException, e:
        ledall_off()
    
    if not (len(in_byte) is SERIAL_READ_BYTE) :
        return 0
        # sometimes, 12 byte alighn is in-correct
        # espacially run on /etc/rc.local
    if not in_byte[9] is 'm':
        shift_byte = checkAlignment(in_byte)
        in_byte = shift_byte
    if ('ppm' in in_byte):
        if not (in_byte[2] is ' ') :
            ppm += (int(in_byte[2])) * 1000
        if not (in_byte[3] is ' ') :
            ppm += (int(in_byte[3])) * 100
        if not (in_byte[4] is ' ') :
            ppm += (int(in_byte[4])) * 10
        if not (in_byte[5] is ' ') :
            ppm += (int(in_byte[5]))
    
    if ppm < 800 :
        ledblue_on()
    elif ppm < 1000 :
        ledbluegreen_on()
    elif ppm < 1300 :
        ledgreen_on()
    elif ppm < 1600:
        ledwhite_on()
    elif ppm < 1900:
        ledyellow_on()
    elif ppm >= 1900 :
        ledpurple_on()
        
    return ppm
