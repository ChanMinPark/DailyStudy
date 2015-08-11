#< TableBar Project >  

####**1. 개요**  
연구실/회사 같은 작업 공간에서 책상 위에 놓을 TableBar를 개발한다.  
TableBar는 다음과 같은 기능을 제공한다.  

    (1)시계 : 일반적으로 시간을 표시해준다.
    (2)달력 : 월 또는 주 단위의 날짜를 보여주며 일정이 있는 날짜에는 표시가 된다.
    (3)날씨 : 예보날씨, 실외날씨, 출장지 날씨가 표시된다.
    (4)알림 : 알림을 설정한 일정에 대해 LED로 알림을 준다.
    (5)Web Page : web2py를 이용한 웹페이지에서 일정 및 지역을 설정하는 기능을

최종적으로는 Color LCD module을 이용해서 정보를 Display하고 싶지만 현재 가지고 있지 않으므로, 일단 LCD를 통해 Text로만 정보들을 출력한다.  
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
    : DB의 tablebar_schedules 테이블를 삽입, 삭제, 수정, 조회 할 수 있음.  
![](https://github.com/ChanMinPark/DailyStudy/blob/master/RefImage/TableBar_3.jpg)
