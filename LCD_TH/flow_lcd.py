import sys
sys.path.append("../lcd_berepi/lib")
from lcd import *

def main():
  # Initialise display
  lcd_init()
  
  content = "Hello World! Have a nice day^^  "
  content2 = "This is ChanMin. Hello everyone. "
  while True:
    lcd_string('%s' %(content), LCD_LINE_1,1)
    lcd_string('%s' %(content2), LCD_LINE_2,3)
    time.sleep(1)
    temp_content = content[:1]
    content = content[1:]
    content += temp_content
    temp_content2 = content2[-1:]
    temp_content2 += content2[:-1]
    content2 = temp_content2
    

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
