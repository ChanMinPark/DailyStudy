#!/usr/bin/python
# Author : ipmstyle, https://github.com/ipmstyle
#        : jeonghoonkang, https://github.com/jeonghoonkang
#        : Kowonsik, https://github.com/kowonsik
#        : ChanMinPark, https://github.com/ChanMinPark
#######################################################
# This file have to be placed in BerePi/apps/sht_lcd/ #
#######################################################

# for the detail of HW connection, see lcd_connect.py

import serial,os
import sys
import RPi.GPIO as GPIO
import logging
import logging.hanlders
import fcntl, socket, struct
sys.path.append("../lcd_berepi/lib")
from lcd import *
import smbus
import time
import requests
import json
sys.path.append("../BereCO2/lib")
from co2led import *

SHT20_ADDR = 0x40       # SHT20 register address
#SHT20_CMD_R_T = 0xE3   # hold Master Mode (Temperature)
#SHT20_CMD_R_RH = 0xE5  # hold Master Mode (Humidity)
SHT20_CMD_R_T = 0xF3    # no hold Master Mode (Temperature)
SHT20_CMD_R_RH = 0xF5   # no hold Master Mode (Humidity)
#SHT20_WRITE_REG = 0xE6 # write user register 
#SHT20_READ_REG = 0xE7  # read user register 
SHT20_CMD_RESET = 0xFE  # soft reset

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEBUG_PRINT = 1
SERIAL_READ_BYTE = 12
FILEMAXBYTE = 1024 * 1024 * 100 #100MB
LOG_PATH = '/home/pi/log_tos.log'

CO2LED_BLUE_PIN = 17
CO2LED_GREEN_PIN = 22
CO2LED_RED_PIN = 27

# important, sensorname shuould be pre-defined, unique sensorname
sensorname = "co2.test"

url = "http://127.0.0.1:4242/api/put"

def main():
  # set logger file
  logger = logging.getLogger(sensorname)
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=FILEMAXBYTE,backupCount=10)
  fileHandler.setLevel(logging.DEBUG)
  fileHandler.setFormatter(formatter)
  logger.addHandler(fileHandler)

  # call raspi init...
  init_process()

  # open RASPI serial device, 38400
  try: 
    serial_in_device = serial.Serial('/dev/ttyAMA0',38400)
  except serial.SerialException, e:
    logger.error("Serial port open error") 
    ledall_off()

  # Initialise display
  lcd_init()
  whiteLCDon()
  print ip_chk(), wip_chk(), mac_chk(), wmac_chk(), stalk_chk()

  while True:
    lcd_string('IP address ', LCD_LINE_1,1)
    lcd_string('MAC eth0, wlan0',LCD_LINE_2,1)
    #blue_backlight(False) #turn on, yellow
    time.sleep(2.5) # 3 second delay

    #Print eth ip and mac address.
    str = ip_chk()
    str = str[:-1]
    lcd_string('%s ET' %str,LCD_LINE_1,1)
    str = mac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    #red_backlight(False) #turn on, yellow
    time.sleep(3.5) # 3 second delay

    #Print wlan ip and mac address.
    str = wip_chk()
    str = str[:-1]
    lcd_string('%s WL     ' % (str),LCD_LINE_1,1)
    str = wmac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    #green_backlight(False) #turn on, yellow
    time.sleep(3.5) # 5 second delay
        
    #Print stalk information.
    str = stalk_chk()
    str = str[:-1]
    lcd_string('sTalk Channel' ,LCD_LINE_1,1)
    lcd_string('%s           ' % (str),LCD_LINE_2,1)
    #red_backlight(False) #turn on, yellow
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
    numTemp = float(value[0])
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
    #url = "http://127.0.0.1:4242/api/put"
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

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' %ord(char) for char in info[18:24]])

macAddr = getHwAddr('eth0')
macAddr = macAddr.replace(':','.')

level = 0
ppm = 0

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
    
def init_process():
    print " "
    print "MSG - [S100, T110 CO2 Sensor Driver on RASPI2, Please check log file : ", LOG_PATH
    print "MSG - now starting to read SERIAL PORT"
    print " "
    ledall_off()

def run_co2_code():
  ppm = 0
  try:
    in_byte = serial_in_device.read(SERIAL_READ_BYTE) 
    pos = 0
    except serial.SerialException, e:
      ledall_off()
    if not (len(in_byte) is SERIAL_READ_BYTE) : 
      logger.error("Serial packet size is strange, %d, expected size is %d" % (len(in_byte),SERIAL_READ_BYTE))
      print 'serial byte read count error'
      continue
    # sometimes, 12 byte alighn is in-correct
    # espacially run on /etc/rc.local
    if not in_byte[9] is 'm':
      shift_byte = checkAlignment(in_byte)
      in_byte = shift_byte
    if ('ppm' in in_byte):
      if DEBUG_PRINT :
        print '-----\/---------\/------ DEBUG_PRINT set -----\/---------\/------ '
          for byte in in_byte :
          #    print "serial_in_byte[%d]: " %pos,
            pos += 1
            if ord(byte) is 0x0d :
          #        print "escape:", '0x0d'," Hex: ", byte.encode('hex')
              continue
            elif ord(byte) is 0x0a :
          #        print "escape:", '0x0a'," Hex: ", byte.encode('hex')
              continue
          #    print " String:", byte,  "    Hex: ", byte.encode('hex')
      if not (in_byte[2] is ' ') :
        ppm += (int(in_byte[2])) * 1000
      if not (in_byte[3] is ' ') :
        ppm += (int(in_byte[3])) * 100
      if not (in_byte[4] is ' ') :
        ppm += (int(in_byte[4])) * 10
      if not (in_byte[5] is ' ') :
        ppm += (int(in_byte[5]))  

      logline = sensorname + ' CO2 Level is '+ str(ppm) + ' ppm' 
      ledall_off()

      if DEBUG_PRINT :
        print logline

      if ppm > 2100 : 
        logger.error("%s", logline)
        # cancel insert data into DB, skip.... since PPM is too high,
        # it's abnormal in indoor buidling
        ledred_on()
        ### maybe change to BLINK RED, later
        continue
      else :
        logger.info("%s", logline)

      print "macAddr : " + macAddr
      
      data = {
        "metric": "rc1.co2.ppm",
        "timestamp": time.time(),
        "value": ppm,
        "tags": {
          "eth0": macAddr,
          "hw": "raspberrypi2" ,
          "sensor" : "co2.t110",
          "name" : sensorname,
          "floor_room": "10fl_min_room",
          "building": "woosung",
          "owner": "kang",
          "country": "kor"
         }
         #tags should be less than 9, 8 is alright, 9 returns http error
      }
    # level = 1, 0~800 ppm,     blue- LED
    # level = 2, 800~1000 ppm,  blue green - LED
    # level = 3, 1000~1300 ppm, green - LED
    # level = 4, 1300~1600 ppm, white - LED
    # level = 5, 1600~1900 ppm, yellow - LED
    # level = 6, 1900~ 2100 ppm,     purple - LED, if over 2100 - red LED

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

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
