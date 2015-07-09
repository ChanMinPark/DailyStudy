import time
from hue import *

def main():
  print getState(2)
  time.sleep(2)

  hue_off(2)
  time.sleep(5)
  
  hue_on(2)
  time.sleep(5)
  
  hue_putHue(2, 43210)
  time.sleep(5)
  
  hue_alert(2, 1)
  print getState(2)
  time.sleep(5)
  
  hue_alert(2, 0)
  print getState(2)
  time.sleep(5)
  
if __name__ == '__main__':
  main()
