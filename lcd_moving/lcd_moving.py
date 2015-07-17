#Author : ChanMin Park, https://github.com/ChanMinPark
#Abstract : The character is moved based on user input.

import sys
from lcd import *
import curses

#Position of Character
characterLine=0
characterPos=0

#Position of Target
targetPos=0

#Line Text
line_f="                "
line_s="                "

def main():
  initWord()
  time.sleep(5)
  line_f="                "
  printToLCD()
  

def initWord():
  #write codes
  line_f = " Get the Target "
  line_s = "       @        "
  characterLine=2
  characterPos=7
  
  printToLCD()

def pressUpKey():
  #write codes
  if characterLine != 1:
    line_f[characterPos] = line_s[characterPos]
    line_s[characterPos] = " "
    characterLine = characterLine - 1
    
    printToLCD()
  
def pressDownKey():
  #write codes
   if characterLine != 2:
    line_s[characterPos] = line_f[characterPos]
    line_f[characterPos] = " "
    characterLine = characterLine + 1
    
    printToLCD()
  
def pressRightKey():
  #write codes
  if characterPos != 15:
    if characterLine == 1:
      line_f[characterPos+1] = line_f[characterPos]
      line_f[characterPos] = " "
    else:
      line_s[characterPos+1] = line_s[characterPos]
      line_s[characterPos] = " "
    characterPos = characterPos + 1
    printToLCD()

def pressLeftKey():
  #write codes
  if characterPos != 0:
    if characterLine == 1:
      line_f[characterPos-1] = line_f[characterPos]
      line_f[characterPos] = " "
    else:
      line_s[characterPos-1] = line_s[characterPos]
      line_s[characterPos] = " "
    characterPos = characterPos - 1
    printToLCD()
  
def printToLCD():
  #write codes
  lcd_string('%s' %(line_f), LCD_LINE_1,1)
  lcd_string('%s' %(line_s), LCD_LINE_2,1)
  
#def changeColor():
  #write codes

#def locateTarget():
  #write codes


#if __name__ == '__main__':
try:
    # Initialise display
    lcd_init()
    
    # get the curses screen window
    stdscr = curses.initscr()
    # turn off input echoing
    curses.noecho()
    # respond to keys immediately (don't wait for enter)
    curses.cbreak()
    # map arrow keys to special values
    stdscr.keypad(True)
    
    main()
  except KeyboardInterrupt:
    pass
  finally:
    # shut down cleanly
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
