#< TableBar Project >  

###1. 개요  
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

####**4. MindMap**  
(* Coggle)  
https://coggle.it/diagram/Vb69jbF6k29HmWtm/3a53c5c49a01a4adf0150bce7358cc725d32ede4754a01e4a2e2f46f801dd106  
