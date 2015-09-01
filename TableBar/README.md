#< TableBar Project >  
(!!!!!Table Bar의 개발 코드는 [web2py의 myapp](https://github.com/ChanMinPark/web2py/tree/master/applications/myapp) 어플리케이션으로 병합되어서 이곳의 코드는 업데이트되지 않음. 하지만 Table Bar의 시스템 설계는 이곳에 설명됨.)  
####**1. 개요**  
연구실/회사 같은 작업 공간에서 책상 위에 놓을 TableBar를 개발한다.  

TableBar 프로젝트의 구성요소는 아래 3가지이다.  
    - TableBar 본체 : 정보 제공의 주체이며 TableBar 프로그램이 실행된다.  
    - Web Page : TableBar에 정보를 표시하기 위한 기본 정보를 설정한다.  
    - Sensor Device : 온도, 습도, 조도, 강수 정보를 센싱하여 Web Server로 전송하여 DB에 저장하게 한다.  

TableBar는 다음과 같은 기능을 제공한다.  

    (1)시계 : 일반적으로 시간을 표시해준다.
    (2)달력 : 월 또는 주 단위의 날짜를 보여주며 일정이 있는 날짜에는 표시가 된다.
    (3)날씨 : 예보날씨, 실외날씨, 출장지 날씨가 표시된다.
              날씨정보의 소스로는 네이버 날씨와, Sensor Device를 복합적으로 이용한다.
    (4)주식 : 관심 종목들을 보여준다.
    (5)스포츠 : 관심 야구팀이 경기중일때 스코어를 보여준다.
    (6)알림 : 알림을 설정한 일정에 대해 LED로 알림을 준다.
              스포츠(스코어 or 경기 결과)에 대해 LED알림을 준다.(정보도 LCD에 출력)
              날씨 변경에 대해 LED 및 LCD 알림을 준다.
    
TableBar의 인터페이스는 아래와 같다.

    (1) 외부 버튼 : 1개 또는 2개의 물리적버튼을 통해서 디스플레이의 화면전환 및 출력화면모드를 선택한다.
                    버튼이 눌릴때의 동작과, 오랫동안 입력이 없을때의 동작을 고려하자.
                    (ex. 오랫동안 입력이 없을 경우 기본화면(시계)으로 표시)
    (2) Web Page : web2py를 이용하여 TableBar에서 필요한 기본정보를 설정할 수 있는 Web Page를 만든다.
                  지역(날씨정보), 일정, 주식(관심종목 등록), 스포츠(관심 야구팀 등록)
                  표시할 화면모드 선택(ex. 주식에 관심이 없으면 주식은 표시하지 않도록 설정)

최종적으로는 Color LCD module을 이용해서 정보를 Display하고 싶지만 현재 가지고 있지 않으므로, 일단 LCD를 통해 Text로만 정보들을 출력한다.  
(2015.08.12 백정엽 교수님 조언으로 LCD를 통한 출력말고 물리적인 디자인으로 표시해도 좋을 것 같다. 예를 들면 날씨를 알릴때 원으로 된 판에 여러 날씨가 표시되어 있고 바늘이 현재 날씨를 가리키는 방식으로.  
그래서 아래 사진과 같은 모양을 구상함. 윗면 시계는 항상 사용자 방향으로 유지. 아랫쪽에 받침대를 두고 받침대에 라즈베리파이를 둠. 삼각기둥이 회전.)  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_future_2.jpg)

그리고 TableBar와는 별도로 실외 날씨 정보를 측정할 Sensor Device를 만든다. Sensor Device는 다음과 같은 값을 측정한다.  

   - 온도
   - 습도
   - 조도
   - 강수(Rain Sensor)

위의 4개의 측정치와 일출, 일몰시간과 기상예보 정보를 토대로 실외 상황을 판단한다.(추후 정확한 판단 알고리즘 고안)

####**2. 장점**  
- 외부 날씨를 확인하기 어려운 실내 환경에서 외부의 날씨를 확인할 수 있다.  
- 책상에서 업무를 보다가 일정을 잊는 경우를 줄인다.  
- 출장지의 날씨를 미리 파악하여 대비할 수 있다.  

####**3. 단점**  
- 출장지에 Sensor Device가 없으면 출장지의 실제 날씨를 파악할 수 없다.
- TableBar에 전력을 공급하기 위해 전원선을 사용해야해서 책상을 어지럽힐 수 있다.

####**4. MindMap**  
(* Coggle)  
https://coggle.it/diagram/Vb69jbF6k29HmWtm/3a53c5c49a01a4adf0150bce7358cc725d32ede4754a01e4a2e2f46f801dd106  

####**5. 진행**
- 달력, 시계, 날씨, Web, Alarm, Sensor 에 대해 각각 파일에 python코드를 작성하여 모듈화한다.  
- 시계 모듈 구현.  
    : getNow() : 현재 시간 정보를 가져옴.  
    : getData() : XXXX-XX-XX-XXX(년-월-일-요일)  
    : getTime() : XX:XX:XX(시:분:초)  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_2.jpg)
- 달력 모듈 구현.  
    : getWeek() : 이번 주의 날짜를 가져옴.  
    : LCD가 2줄이기 때문에 한주 단위로 출력  
    : 윗줄-요일표시, 아랫줄 - 날짜표시  
    : 두자리 수의 날짜가 있는 주에는 칸이 부족. 그래서 길게 흐르는 문자열로 구현.  
    : 달의 경계가 있는 주에는 날짜 주의(ex. 30,31,1,2,3)  
    : web2py로 구현한 웹서버에서 일정을 받아와서 일정이 있는 날에는 표시(*).  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_1.jpg)
- 달력 모듈 전에 달력에 '일정있음'표시를 위하여 web2py의 DB를 먼저 구현.  
    : DB에 tablebar_schedules 테이블을 생성.  
    : date, location, content, isAlarm 필드를 생성.  
    : 달력 모듈에서 DB에 접근하여 일정을 받아서 달력에 표시 할 예정.  
- Web Page  
    : Table Bar Setting Page 제작  
    : DB의 tablebar_schedules 테이블를 삽입, 삭제, 수정, 조회 할 수 있음.(일정)  
    : DB의 tablebar_user_loctaion 테이블을 삽입, 삭제, 수정, 조회 할 수 있음.(지역)  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_3.jpg)  
  
- 날씨 모듈 구현.  
    : 네이버 날씨를 가져옴.  
    : web2py로 만든 웹서버를 이용하여 지역을 설정하고 이를 DB에 저장함.  
    : getWeather() : web에 설정한 지역을 가져와서 네이버 날씨의 예보를 가져옴.(기온, 날씨)  
    **(구현중...네이버 날씨 정보를 가져오는 과정에서 html문서를 읽어올수가 없음. 안랩에이전트 때문에...)**  
  
- LCD 모듈을 pcb판에 결합하여 모양을 새로 잡음.  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/new_shape.jpg)
- web2py와 TableBar 프로그램을 개별적으로 개발하던 것을 web2py의 cron기능을 이용하여 web2py로 병합함.  
    : 기존에 TableBar 프로그램에서 web2py의 페이지 html코드를 긁어오던 것을, 바로 DB 연결하도록 코드 수정 필요.  
    : 지역, 일정을 가져오는 부분이 수정이 필요함.  
    : [cron 기능 사용하기](http://walkinpcm.blogspot.kr/2015/08/web2py-cron.html)  
    : cron으로 실행한 python 코드에서 web2py의 global 변수를 사용할 수 있는 방법을 찾으려 하였는데 알아내지 못하여 module에 전역변수로 사용할 변수를 선언하고 setter와 getter로 접근하기로 함. (cron으로 실행하는 py파일도 web2py의 module에 있는 함수에 접근 할 수 있음을 이용.)  
    : module에 global 변수를 사용하는 것도 cron과 web2py가 공용으로 사용할 수 있는 변수로 사용하는 것은 실패하였다. 그래서 제일 확실하게 DB에 공용으로 사용 하고 싶은 변수를 저장하였다. 중요한 점은 **DB에 값을 삽입,변경,삭제 할 경우에는 commit을 꼭 해줘야 한다는 점이다.**  

- 스포츠(야구) 정보 출력.  
    : 관심 야구팀을 등록.(ㅇ)  
    : 프로야구 시즌에만 정보를 출력.(시즌이 아니면 시즌이 아니라고 띄움)(ㅇ)  
    : 관심 야구팀이 경기를 시작하면 알림.(ㅅ)  
    : 관심 야구팀의 경기가 스코어가 변경될때마다 알림.  
    : 관심 야구팀의 경기가 끝나면 최종 스코어를 출력하며 동시에 알림.  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_4.jpg)

- Raspberry Pi 가 부팅 될때 web2py도 같이 실행하기.  


      #####################################################################  
      # Run web2py with TableBar  
      #####################################################################  
      echo "Run web2py with TableBar"  
      cd /usr/local/web2py  
      echo ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1  
      _WIP=$(ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1)  
      printf "%s\n" "$_WIP"  
      sudo python web2py.py -i "$_WIP" -p 8000 -a 'tinyos' -c server.crt -k server.key -Y &  
      cd  

- 알림.  
    : 알림을 주는 상황에 따라 각각 다른 알림을 구현.  
    : 알림을 주는 상황  
      (1) 등록된 일정의 시간이 되었을 때: 초록불이 깜박인다.  
      (2) 야구팀이 경기를 시작할때, 스코어가 변경될 때, 경기가 종료 될 때**(경기시간에 확인필요)**  
          (2-1) 경기 시작, 끝 : 빨간불이 깜박인다.  
          (2-2) 스코어 변경 : 빨강, 노랑, 분홍 불이 깜박인다.  

- LCD에 출력되는 문장을 파일에 출력하도록 함. 추후 이 파일을 메일로 주기적으로 보내게 하여 상태확인에 사용할 예정.  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_5.jpg)

####**6. 추후 개발 계획**  

log파일을 메일로 보내게 하기 위해서 mailgun에 대하여 알아본다.
