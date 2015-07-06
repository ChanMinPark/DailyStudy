#!/usr/bin/python
# Author : ChanMinPark, https://github.com/ChanMinPark

import sys
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

def main():
  lcd_init()
  print "Hello ChanMin"
  
  while True:
    #Write Temp/Humi getting code and printing code
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
    time.sleep(1)
    

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
