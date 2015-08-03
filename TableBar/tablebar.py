import sys
sys.path.append("./lib")
from lcd import *
from tablebar_time import *

def main():
  # Initialise display
  lcd_init()
  
  while True:
    # Display date & time
    lcd_string(getData(), LCD_LINE_1, 2)
    lcd_string(getTime(), LCD_LINE_2, 2)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
