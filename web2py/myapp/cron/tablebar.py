from lcd import *
from tablebar_time import *
from tablebar_calender import *
from tablebar_weather import *
from tablebar_globals import *

def main():
    # Initialise display
    lcd_init()
    whiteLCDon()
    
    r_time = 0
    while True:#r_time >= 0:
        lcd_string("Cron Test", LCD_LINE_1, 2)
        lcd_string("%d, %d"%(getTask(), r_time), LCD_LINE_2, 2)
        r_time = r_time + 1
        time.sleep(1)
    
    """ 
    while True:
        # Display date & time
        lcd_string(getData(), LCD_LINE_1, 2)
        lcd_string(getTime(), LCD_LINE_2, 2)
    
    while True:
        # Display calender
        plines = getWeek()
        cycle = 5
        while cycle > 0:
            time.sleep(2)
            lcd_string(plines[0], LCD_LINE_1, 1)
            lcd_string(plines[1], LCD_LINE_2, 1)
            plines[0] = plines[0][:4]+plines[0][8:]
            plines[1] = plines[1][:4]+plines[1][8:]
            cycle = cycle - 1
  
    
    while True:
        data = {}a
        data = getWeather()
        lcd_string("Now : "+data['now_temp']+"'C, "+data['now_weather'], LCD_LINE_1, 2)
        lcd_string("1h : "+data['one_later']+", 2h : "+data['two_later'], LCD_LINE_2, 2)
        time.sleep(5)
    """
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!",LCD_LINE_1,2)
	#lcd_string("%d"%(session.which_task),LCD_LINE_2,2)
        GPIO.cleanup()
