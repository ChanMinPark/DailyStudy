# -*- coding: utf-8 -*-

import time
import random
from hue import *

def main():
  lights=[1,2,3]
  
  for lightnum in lights:
    print getState(lightnum)
  time.sleep(7)
  
  for lightnum in lights:
    hue_putHue(lightnum,0)
    hue_putSat(lightnum,0)

  for lightnum in lights:
    hue_off(lightnum)
    time.sleep(5)
  time.sleep(3)
  
  for lightnum in lights:
    hue_on(lightnum)
    hue_putSat(lightnum,255)
    hue_effect(lightnum, 1)
  time.sleep(15)
  for lightnum in lights:
    hue_effect(lightnum, 0)
  
  for lightnum in lights:
    hue_off(lightnum)
  time.sleep(5)
  
  for lightnum in lights:
    hue_on(lightnum)
    hue_putSat(lightnum,0)
    hue_alert(lightnum, 2)
  time.sleep(10)
  for lightnum in lights:
    hue_alert(lightnum, 0)
  
  for lightnum in lights:
    random_bri = random.randrange(0,65535) #0~65535 사이의 정수 랜덤으로 출력
    hue_putHue(lightnum, random_bri)
  
  for lightnum in lights:
    print getState(lightnum)
  """
  hue_off(2)
  time.sleep(5)
  
  hue_on(2)
  time.sleep(5)
  
  hue_putHue(2, 43210)
  time.sleep(5)
  
  hue_alert(2, 2)
  print getState(2)
  time.sleep(15)
  
  hue_alert(2, 0)
  print getState(2)
  time.sleep(5)
  
  hue_effect(2, 1)
  print getState(2)
  time.sleep(15)
  
  hue_effect(2, 0)
  print getState(2)
  time.sleep(5)
  """
  
if __name__ == '__main__':
  main()
