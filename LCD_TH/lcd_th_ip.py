#!/usr/bin/python
# Author : ipmstyle, https://github.com/ipmstyle
#        : jeonghoonkang, https://github.com/jeonghoonkang
#        : ChanMinPark, https://github.com/ChanMinPark
#######################################################
# This file have to be placed in BerePi/apps/sht_lcd/ #
#######################################################

# for the detail of HW connection, see lcd_connect.py

import sys
sys.path.append("../lcd_berepi/lib")
from lcd import *
import smbus
import time
import requests
import json

SHT20_ADDR = 0x40       # SHT20 register address
#SHT20_CMD_R_T = 0xE3   # hold Master Mode (Temperature)
#SHT20_CMD_R_RH = 0xE5  # hold Master Mode (Humidity)
SHT20_CMD_R_T = 0xF3    # no hold Master Mode (Temperature)
SHT20_CMD_R_RH = 0xF5   # no hold Master Mode (Humidity)
#SHT20_WRITE_REG = 0xE6 # write user register 
#SHT20_READ_REG = 0xE7  # read user register 
SHT20_CMD_RESET = 0xFE  # soft reset

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

def main():
  # Initialise display
  lcd_init()
  print ip_chk(), wip_chk(), mac_chk(), wmac_chk(), stalk_chk()

  while True:
    lcd_string('IP address ', LCD_LINE_1,1)
    lcd_string('MAC eth0, wlan0',LCD_LINE_2,1)
    blue_backlight(False) #turn on, yellow
    time.sleep(2.5) # 3 second delay

    #Print eth ip and mac address.
    str = ip_chk()
    str = str[:-1]
    lcd_string('%s ET' %str,LCD_LINE_1,1)
    str = mac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    red_backlight(False) #turn on, yellow
    time.sleep(3.5) # 3 second delay

    #Print wlan ip and mac address.
    str = wip_chk()
    str = str[:-1]
    lcd_string('%s WL     ' % (str),LCD_LINE_1,1)
    str = wmac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    green_backlight(False) #turn on, yellow
    time.sleep(3.5) # 5 second delay
        
    #Print stalk information.
    str = stalk_chk()
    str = str[:-1]
    lcd_string('sTalk Channel' ,LCD_LINE_1,1)
    lcd_string('%s           ' % (str),LCD_LINE_2,1)
    red_backlight(False) #turn on, yellow
    time.sleep(3.5) # 5 second delay
    
    #Print temp and humi information on LCD.
    temp = reading(1)
    humi = reading(2)
    if not temp or not humi:
        print "register error"
        break
    value = calc(temp, humi)
    send2tsdb(value[0],value[1])
    #print "temp : %s\thumi : %s" % (value[0], value[1])
    lcd_string('Temp : %s' % (value[0]),LCD_LINE_1,1)
    lcd_string('Humi : %s' % (value[1]),LCD_LINE_2,1)
    #Turn on the led based on temperature
    numTemp = fload(value[0])
    if (numTemp < 21) :
      blueLCDon()
    elif (numTemp < 24) :
      skyeLCDon()
    elif (numTemp < 27) :
      greenLCDon()
    elif (numTemp < 29) :
      yellowLCDon()
    else :
      redLCDon()
    time.sleep(3.5)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def ip_chk():
    cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    ipAddr = run_cmd(cmd)
    return ipAddr

def wip_chk():
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    wipAddr = run_cmd(cmd)
    return wipAddr

def mac_chk():
    cmd = "ifconfig -a | grep ^eth | awk '{print $5}'"
    macAddr = run_cmd(cmd)
    return macAddr

def wmac_chk():
    cmd = "ifconfig -a | grep ^wlan | awk '{print $5}'"
    wmacAddr = run_cmd(cmd)
    return wmacAddr

def stalk_chk():
    cmd = "hostname"
    return run_cmd(cmd)
    
#According to v value, this function return raw temp or humi data.
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

#Calculate temp and humi data using row data.
def calc(temp, humi):
    tmp_temp = -46.85 + 175.72 * float(temp) / pow(2,16)
    tmp_humi = -6 + 125 * float(humi) / pow(2,16)

    return tmp_temp, tmp_humi

#Send temp and humi data to TSDB
def send2tsdb(temp, humi):
    url = "http://127.0.0.1:4242/api/put"
    data = {
      "metric": "pcm.temp",
      "timestamp": time.time(),
      "value": float(temp),
      "tags": {
         "host": "raspi-pcm"
      }
    }
    ret = requests.post(url, data=json.dumps(data))
    #print ret.text
    
    data = {
      "metric": "pcm.humi",
      "timestamp": time.time(),
      "value": float(humi),
      "tags": {
         "host": "raspi-pcm"
      }
    }
    ret = requests.post(url, data=json.dumps(data))
    #print ret.text


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
