#Author : ChanMin Park, https://github.com/ChanMinPark
#Abstract : The character is moved based on user input.

import sys
from lcd import *
import curses

#Position of Character
characterLine=0
characterPos=0

def main():
  # get the curses screen window
  stdscr = curses.initscr()
  # turn off input echoing
  curses.noecho()
  # respond to keys immediately (don't wait for enter)
  curses.cbreak()
  # map arrow keys to special values
  stdscr.keypad(True)
  
  finally:
    # shut down cleanly
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    
def initWord():
  #write codes

def pressUpKey():
  #write codes
  
def pressDownKey():
  #write codes
  
def pressRightKey():
  #write codes

def pressLeftKey():
  #write codes
  
def printToLCD():
  #write codes
