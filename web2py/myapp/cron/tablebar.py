from lcd import *
from tablebar_time import *
from tablebar_calender import *
from tablebar_weather import *
#from tablebar_globals import *
from gluon import current

def main():
    # Display time information
    cycle = 10
    while current.whichtask == 0:
    	if cycle == 0:
    	    current.whichtask = 1
    	    break
    	if current.islock == False:
    	    current.islock = True
    	    # Display date & time
    	    lcd_string(getData(), LCD_LINE_1, 2)
    	    lcd_string(getTime(), LCD_LINE_2, 2)
    	    cycle = cycle - 1
    	    time.sleep(1)
    	    current.islock = False
    
    # Display date information
    while current.whichtask == 1:
        # Display calender
        plines = getWeek()
        cycle = 5
        if current.islock == False:
            current.islock = True
            while cycle > 0:
                time.sleep(1)
                lcd_string(plines[0], LCD_LINE_1, 1)
                lcd_string(plines[1], LCD_LINE_2, 1)
                plines[0] = plines[0][:4]+plines[0][8:]
                plines[1] = plines[1][:4]+plines[1][8:]
                cycle = cycle - 1
                time.sleep(1)
            current.islock = False
        if cycle == 0:
            current.whichtask = 0
            break
  
    """
    while True:
        data = {}a
        data = getWeather()
        lcd_string("Now : "+data['now_temp']+"'C, "+data['now_weather'], LCD_LINE_1, 2)
        lcd_string("1h : "+data['one_later']+", 2h : "+data['two_later'], LCD_LINE_2, 2)
        time.sleep(5)
    """
if __name__ == '__main__':
    try:
    	# Initialise display
        lcd_init()
        whiteLCDon()
        current.whichtask = 0
        current.islock = False
        
        while True:
            main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!",LCD_LINE_1,2)
	#lcd_string("%d"%(session.which_task),LCD_LINE_2,2)
        GPIO.cleanup()
