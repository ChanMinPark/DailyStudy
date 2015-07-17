#Author : ChanMin Park, https://github.com/ChanMinPark
#Abstract : The character is moved based on user input.

import sys
from lcd import *
import curses
import thread

#Position of Character
characterLine=0
characterPos=0
  
#Position of Target
targetPos=0

#Line Text
line_f="                "
line_s="                "

#game time
gtime = 30

def main():
  global line_f, gtime
  
  initWord()
  time.sleep(5)
  line_f="                "
  printToLCD()
  
  thread.start_new_thread(gameTimer, (30,))
  
  while gtime > 0:
    char = stdscr.getch()
    if char == curses.KEY_UP:
      pressUpKey()
    elif char == curses.KEY_DOWN:
      pressDownKey()
    elif char == curses.KEY_RIGHT:
      pressRightKey()
    elif char == curses.KEY_LEFT:
      pressLeftKey()
  
  lcd_string('Game', LCD_LINE_1,2)
  lcd_string('Over', LCD_LINE_2,2)
  time.sleep(3)

def initWord():
  global line_f, line_s, characterLine, characterPos
  line_f = " Get the Target "
  line_s = "       @        "
  characterLine=2
  characterPos=7
  
  printToLCD()

def pressUpKey():
  global line_f, line_s, characterLine, characterPos
  if characterLine != 1:
    line_f = line_f[:characterPos]+line_s[characterPos:characterPos+1]+line_f[characterPos+1:]
    line_s = line_s[:characterPos]+" "+line_s[characterPos+1:]
    characterLine = characterLine - 1
    
    printToLCD()
  
def pressDownKey():
  global line_f, line_s, characterLine, characterPos
  if characterLine != 2:
    line_s = line_s[:characterPos]+line_f[characterPos:characterPos+1]+line_s[characterPos+1:]
    line_f = line_f[:characterPos]+" "+line_f[characterPos+1:]
    characterLine = characterLine + 1
    
    printToLCD()
  
def pressRightKey():
  global line_f, line_s, characterLine, characterPos
  if characterPos != 13:
    if characterLine == 1:
      line_f = line_f[:characterPos]+" "+line_f[characterPos:characterPos+1]+line_f[characterPos+2:]
    else:
      line_s = line_s[:characterPos]+" "+line_s[characterPos:characterPos+1]+line_s[characterPos+2:]
    characterPos = characterPos + 1
    printToLCD()

def pressLeftKey():
  global line_f, line_s, characterLine, characterPos
  if characterPos != 0:
    if characterLine == 1:
      line_f = line_f[:characterPos-1]+line_f[characterPos:characterPos+1]+" "+line_f[characterPos+1:]
    else:
      line_s = line_s[:characterPos-1]+line_s[characterPos:characterPos+1]+" "+line_s[characterPos+1:]
    characterPos = characterPos - 1
    printToLCD()
  
def printToLCD():
  global line_f, line_s, gtime
  lcd_string('%s%2d' %(line_f, gtime), LCD_LINE_1,1)
  lcd_string('%s' %(line_s), LCD_LINE_2,1)
  
def gameTimer(initTime):
  global gtime
  gtime = initTime
  while gtime > 0:
    time.sleep(1)
    gtime = gtime - 1
    
  
  
#def changeColor():
  #write codes

#def locateTarget():
  #write codes


if __name__ == '__main__':
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
  try:
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
