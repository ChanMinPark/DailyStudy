##**< 키보드 Input으로 LCD 캐릭터 제어하기 >**

####**1. 개요**
LCD 모듈에 캐릭터 하나를 출력하고, 이를 키보드 방향키로 제어하여 움직이게 한다.  
초기 시작 화면을 보여주고, 캐릭터가 있는 위치를 제외하고 다른 임의의 위치에 타겟을 나타내고 캐릭터가 해당 타겟까지 이동해서 타겟을 먹으면 다음 타겟이 나타나게 한다. 타겟을 먹을때 LCD의 색이 반짝인다.  

####**2. Python에서 사용자 입력 받기**
Python에서 기본적으로 제공하는 사용자 입력 방법은 2가지가 있다.  
하나는 input()이고, 다른 하나는 raw_input()이다. 둘다 입력이지만 조금의 차이가 있다.  
raw_input()은 엔터입력 전까지 입력받는 것을 문자열로 반환한다. 반면에 input()은 입력받은 문자를 eval()함수로 처리하여 반환한다.  
하지만 input()과 raw_input()은 키보드의 문자열을 입력받는 함수이다.  
여기에서는 키보드 방향키 입력이 필요하므로 위의 두 함수는 사용하지 않는다.  
본 프로젝트에서는 키 입력에 대해서 2가지 요구조건이 있다.  
	- 방향키 입력이 가능해야한다.
	- 엔터키를 누르지 않고 바로 인식이 되어야 한다.
해당 요구조건을 만족하기 위해서 본 프로젝트에서는 Python의 Curses 라이브러리를 이용한다.  
(Curses 라이브러리 설명 : https://docs.python.org/2/howto/curses.html)

Curses를 사용하기 위해 먼저 import 한다.

	import curses
그리고 초기화를 시켜준다. iniscr함수로 초기화를 하고 window를 반환받는다.

	stdscr = curses.initscr()
입력한 키를 출력하지 않기 위해서 noecho함수를 쓴다.

	curses.noecho()
엔터를 치지 않고 바로 입력받기 위해서 cbreak함수를 쓴다.

	curses.cbreak()
Curses 라이브러리에서는 키마다 고유의 문자상수(?)를 부여했다. 이를 사용하기 위해서는 아래와 같이 써준다.

	stdscr.keypad(True)
Curses를 끝내기위해서 코드가 끝나기 전에 아래와 같이 수행해준다.

	curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()

####**3.코드 작성하기**
아래 링크에 전체 코드가 있다.  
https://github.com/ChanMinPark/DailyStudy/blob/master/lcd_moving/lcd_moving.py  

####**4.실행 결과**
이번 프로젝트의 실행 결과를 동영상으로 제작하여 유튜브에 업로드 하였다.  
[[youtube-{RhdrT6STYZ8}-{688}x{387}]]
