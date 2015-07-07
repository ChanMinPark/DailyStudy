# This file path must be BerePi/apps/sht20/

import smbus
import serial,os
import time
import requests
import json
import sys
import string
import RPi.GPIO as GPIO
import logging
import logging.handlers
import fcntl, socket, struct

sys.path.append("../lcd_berepi/lib")
from lcd import *
sys.path.append("../BereCO2/lib")
from co2led import *

DEBUG_PRINT = 1
SERIAL_READ_BYTE = 12
FILEMAXBYTE = 1024 * 1024 * 100
LOG_PATH = '/home/pi/log_tos.log'

CO2LED_BLUE_PIN = 17
CO2LED_GREEN_PIN = 22
CO2LED_RED_PIN = 27

sensorname = "co2.test"

SHT20_ADDR = 0x40       # SHT20 register address
SHT20_CMD_R_T = 0xF3    # no hold Master Mode (Tmeperature)
SHT20_CMD_R_RH = 0xF5   # no hold Master Mode (Humidity)
SHT20_CMD_RESET = 0xFE  # soft reset

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

level = 0
ppm = 0

def checkAlignment(incoming) :
    idxNum = incoming.find('m')

    offset = idxNum - 9
    if offset > 0 :
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    if offset < 0 :
        offset = 12 + offset
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    return new_str

def init_process() :
    print "MSG - [S100, T110 CO2 Sensor Driver on RASPI2, Please check log file : ", LOG_PATH
    print "MSG - now statring to read SERIAL PORT"
    ledall_off()

def reading(v) :        # read sht20 sensor
    bus.write_quick(SHT20_ADDR)
    if v == 1:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_T)
    elif v == 2:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_RH)
    else :
        return False

    time.sleep(.1)

    b = (bus.read_byte(SHT20_ADDR) <<8)
    b += bus.read_byte(SHT20_ADDR)

    return b

def calc(temp, humi) :
    tmp_temp = -46.85 + 175.72 * float(temp) / pow(2,16)
    tmp_humi = -6 + 125 * float(humi) / pow(2,16)

    return tmp_temp, tmp_humi

def send_data(temp, humi, co2) :
    # send temp data
    url = "http://127.0.0.1:4242/api/put"
    data = {
            "metric": "keti.sht20.temp",
            "timestamp" : time.time(),
            "value" : float(temp),
            "tags":{
                "host": "mgpark"
            }
    }
    ret = requests.post(url, data=json.dumps(data))
    print ret.text

    # send humi data
    data = {
            "metric": "keti.sht20.humi",
            "timestamp" : time.time(),
            "value" : float(humi),
            "tags":{
                "host": "mgpark"
            }
    }
    ret = requests.post(url, data=json.dumps(data))
    print ret.text

    # send co2 data
    data = {
            "metric" : "keti.rc1.co2",
            "timestamp" : time.time(),
            "value" : co2,
            "tags":{
                "host": "mgpark"
            }
    }
    ret = requests.post(url, data=json.dumps(data))
    print ret.text

def backlight_func() :   # Turn On LCD
    temp = reading(1)
    humi = reading(2)
    if not temp or not humi :
        print ( "register error")
    value = calc(temp, humi)
    tempVal = ('%.5s' %value[0])
    humiVal = ('%.5s' %value[1])
    print "temp : %s \t humi : %s" % (tempVal, humiVal)

    lcdVal = float(tempVal)

    if lcdVal < 21 :
        blueLCDon()
    elif lcdVal < 24 :
        skyeLCDon()
    elif lcdVal < 27 :
        greenLCDon()
    elif lcdVal < 29 :
        yellowLCDon()
    else :
        redLCDon()

    return tempVal, humiVal

def lcd_string_sensorVal(temp, humi, co2) :
    lcd_string('Temp : %s' % temp, LCD_LINE_1, 1)
    lcd_string('Humi : %s' % humi, LCD_LINE_2, 1)
    time.sleep(2)

    lcd_string('Co2 : %s' % co2, LCD_LINE_1, 1)
    time.sleep(2)

def lcd_string_ip_addr() :
    lcd_string('IP address ', LCD_LINE_1, 1)
    lcd_string('MAC eth0, wlan0', LCD_LINE_2, 1)
    time.sleep(2)

    backlight_func()
    str = ip_chk()
    str = str[:-1]
    lcd_string('%s ET' % str, LCD_LINE_1, 1)
    str = mac_chk()
    str = str[:-1]
    lcd_string('%s' % str, LCD_LINE_2, 1)
    time.sleep(2)

    backlight_func()
    str = wip_chk()
    str = str[:-1]
    lcd_string('%s WL' % str, LCD_LINE_1, 1)
    str = wmac_chk()
    str = str[:-1]
    lcd_string('%s' % str, LCD_LINE_2, 1)
    time.sleep(2)

    backlight_func()
    str = stalk_chk()
    str = str[:-1]
    lcd_string('sTalk Channel', LCD_LINE_1, 1)
    lcd_string('%s' % str, LCD_LINE_2, 1)
    time.sleep(2)

def run_cmd(cmd) :
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

# Receive address value from shell command
def ip_chk() :
    cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    ipAddr = run_cmd(cmd)
    return ipAddr

def wip_chk() :
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    wipAddr = run_cmd(cmd)
    return wipAddr

def mac_chk() :
    cmd = "ifconfig -a | grep ^eth | awk '{print $5}'"
    macAddr = run_cmd(cmd)
    return macAddr

def wmac_chk() :
    cmd = "ifconfig -a | grep ^wlan | awk '{print $5}'"
    wmacAddr = run_cmd(cmd)
    return wmacAddr

def stalk_chk() :
    cmd = "hostname"
    stalk = run_cmd(cmd)
    return stalk

def readCo2() :
    ppm = 0
    try :
        in_byte = serial_in_device.read(SERIAL_READ_BYTE)
        pos = 0
    except serial.SerialException, e:
        ledall_off()
    if not (len(in_byte) is SERIAL_READ_BYTE) :
        logger.error("Serial packet size is strange, %d, expected size is %d" % (len(in_byte),SERIAL_READ_BYTE))
        print 'serial byte read count error'
        return -1

    if not in_byte[9] is 'm' :
        shift_byte = checkAlignment(in_byte)
        in_byte = shift_byte
    if('ppm' in in_byte):
        if not (in_byte[2] is ' ') :
            ppm += (int(in_byte[2])) * 1000
        if not (in_byte[3] is ' ') :
            ppm += (int(in_byte[3])) * 100
        if not (in_byte[4] is ' ') :
            ppm += (int(in_byte[4])) * 10
        if not (in_byte[5] is ' ') :
            ppm += (int(in_byte[5]))

        logline = sensorname + ' CO2 Level is ' + str(ppm) + ' ppm'
        ledall_off()

        if ppm > 2100 :
            logger.error("%s", logline)
            ledred_on()
            return -1
        else :
            logger.info("%s",logline)

    if ppm < 800 :
        ledblue_on()
    elif ppm < 1000 :
        ledbluegreen_on()
    elif ppm < 1300 :
        ledgreen_on()
    elif ppm < 1600 :
        ledwhite_on()
    elif ppm < 1900 :
        ledyellow_on()
    elif ppm >= 1900 :
        ledpurple_on()

    return ppm

def main() :    
    lcd_init()          # When program start, init lcd
    logger = logging.getLogger(sensorname)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=FILEMAXBYTE, backupCount=10)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    init_process()

    try:
        serial_in_device = serial.Serial('/dev/ttyAMA0', 38400)
    except serial.SerialException, e:
        logger.error("Serial port open error")
        ledall_off()

    print ip_chk(), wip_chk(), mac_chk(), wmac_chk(), stalk_chk()
    while True:
        value = backlight_func()
        if not value[0] or not value[1] :
            break
        tempVal = value[0]
        humiVal = value[1]
        Co2Val = readCo2
        if not Co2Val == -1 :
            lcd_string_sensorVal(tempVal, humiVal, Co2Val)
            lcd_string_ip_addr()

            print "temp : %s \t humi : %s \t co2 : %d " % (tempVal, humiVal, Co2Val)

            send_data(value[0], value[1], Co2Val)
        
if __name__ == '__main__' :
    try :
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1, 2)
        GPIO.cleanup()
        
