import sys
sys.path.append("./lib")
from lcd import *
from tablebar_time import *
from tablebar_calender import *

def main():
  # Initialise display
  lcd_init()
  """
  while True:
    # Display date & time
    lcd_string(getData(), LCD_LINE_1, 2)
    lcd_string(getTime(), LCD_LINE_2, 2)
  """  
  while True:
    # Display calender
    plines = getWeek()
    cycle = 4
    while cycle > 0:
      time.sleep(2)
      lcd_string(plines[0], LCD_LINE_1, 1)
      lcd_string(plines[1], LCD_LINE_2, 1)
      plines[0] = plines[0][:4]+plines[0][8:]
      plines[1] = plines[1][:4]+plines[1][8:]
      cycle = cycle - 1


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
