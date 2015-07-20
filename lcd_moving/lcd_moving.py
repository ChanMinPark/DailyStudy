#Author : ChanMin Park, https://github.com/ChanMinPark
#Abstract : The character is moved based on user input.

import sys
from lcd import *
import curses
import thread
import random

#Position of Character
characterLine=0
characterPos=0
  
#Position of Target
targetLine=0
targetPos=0

#Line Text
line_f="              "
line_s="              "

#game time
gtime = 30
#game score
gscore = 0

#create lock object
lock = thread.allocate_lock()

def main():
  global line_f, gtime, gscore
  
  initWord()
  time.sleep(5)
  line_f = "              "
  #line_s = "       @      "
  printToLCD()
  locateTarget()
  
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
  
  lcd_string('Game Over!', LCD_LINE_1,2)
  lcd_string('%s' %gscore, LCD_LINE_2,2)
  time.sleep(3)

def initWord():
  global line_f, line_s, characterLine, characterPos
  line_f = " Get the Target "
  line_s = "       @      "
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
    catchTarget()
  
def pressDownKey():
  global line_f, line_s, characterLine, characterPos
  if characterLine != 2:
    line_s = line_s[:characterPos]+line_f[characterPos:characterPos+1]+line_s[characterPos+1:]
    line_f = line_f[:characterPos]+" "+line_f[characterPos+1:]
    characterLine = characterLine + 1
    
    printToLCD()
    catchTarget()
  
def pressRightKey():
  global line_f, line_s, characterLine, characterPos
  if characterPos != 13:
    if characterLine == 1:
      line_f = line_f[:characterPos]+" "+line_f[characterPos:characterPos+1]+line_f[characterPos+2:]
    else:
      line_s = line_s[:characterPos]+" "+line_s[characterPos:characterPos+1]+line_s[characterPos+2:]
    characterPos = characterPos + 1
    printToLCD()
    catchTarget()

def pressLeftKey():
  global line_f, line_s, characterLine, characterPos
  if characterPos != 0:
    if characterLine == 1:
      line_f = line_f[:characterPos-1]+line_f[characterPos:characterPos+1]+" "+line_f[characterPos+1:]
    else:
      line_s = line_s[:characterPos-1]+line_s[characterPos:characterPos+1]+" "+line_s[characterPos+1:]
    characterPos = characterPos - 1
    printToLCD()
    catchTarget()
  
def printToLCD():
  global line_f, line_s, gtime, gscore
  lock.acquire()
  lcd_string('%s%2s' %(line_f, gtime), LCD_LINE_1,1)
  lcd_string('%s%2s' %(line_s, gscore), LCD_LINE_2,1)
  lock.release()
  
def gameTimer(initTime):
  global gtime
  gtime = initTime
  while gtime > 0:
    time.sleep(1)
    gtime = gtime - 1
    if lock.locked()==False:
      printToLCD()
    
  
  
#def changeColor():
  #write codes

def locateTarget():
  #write codes
  global characterLine, characterPos, targetLine, targetPos, line_f, line_s
  while True:
    targetLine = random.randrange(1,3)
    targetPos = random.randrange(1,14)
    if targetLine == characterLine:
      if targetPos == characterPos:
        continue
      else:
        if targetLine == 1:
          line_f = line_f[:targetPos]+"$"+line_f[targetPos+1:]
        else:
          line_s = line_s[:targetPos]+"$"+line_s[targetPos+1:]
        break
    else:
      if targetLine == 1:
        line_f = line_f[:targetPos]+"$"+line_f[targetPos+1:]
      else:
        line_s = line_s[:targetPos]+"$"+line_s[targetPos+1:]
      break
  
  printToLCD()
  
def catchTarget():
  global characterLine, characterPos, targetLine, targetPos, gscore
  if characterLine == targetLine:
    if characterPos == targetPos:
      gscore += 1
      locateTarget()



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
