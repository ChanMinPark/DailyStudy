##< Raspberry Pi에 Apache, Tomcat, Mysql 설치하기 >  

###1. JAVA 확인하기.  
Tomcat7이 apt에서 받을 수 있는 최신 버전인데 Tomcat7은 JAVA JDK 1.8에서 동작하지 않는다.(컴파일이 되지 않는다.)  
그래서 JAVA를 1.7로 낮춰주어야한다.  

먼저, JAVA 버전을 확인한다.  

	$javac -version
버전이 1.8로 나오면 아래와 같은 과정으로 1.8을 삭제하고 1.7로 새로 설치한다.  
JAVA를 apt로 설치하였을 경우에 아래 명령어로 삭제 가능하다.  

	$sudo apt-get purge oracle-java8-jdk
purge는 설정까지 모두 지우는 것이다. 설정을 남기려면 remove로 지우면 된다.  
나는 oracle java가 apt로 설치 되어 있었기 때문에 위와 같이 간단하게 지울 수 있었다.  
oracle java 7으로 설치하는 명령어는 아래와 같다.  

	$sudo apt-get install oracle-java7-jdk
설치가 완료되고 JAVA버전을 다시 확인해보면 1.7로 나온다.  
JAVA가 설치되면 환경설정을 해준다. /etc/profile에 추가하거나 쉘에서만 추가해도 된다. Tomcat을 위한 JAVA 환경설정은 Tomcat 설정파일에 다시 해 줄 것이다.  

	$export JAVA_HOME=/usr/lib/jvm/jdk-7-oracle-armhf

###2. Tomcat7 설치하기.  
(출처 : http://yoo7577.tistory.com/204)  
apt로 Tomcat7을 설치한다.

	$sudo apt-get install tomcat7
설치가 완료되면 설치 로그 맨 아래를 잘 보아야한다.  
tomcat7이라는 user와 group이 새로 생긴다. 그리고, 내 경우에는 JAVA_HOME이 제대로 잡히지 않아서 Tomcat7이 설치는 되었지만 JAVA를 못 찾아서 구동은 바로 되지 못하였다.  
![](/RefImage/tomcat_1.JPG)

Tomcat 구동시에 이용하는 환경 설정 파일에 JAVA_HOME을 잡아주어야 한다.  

	$sudo nano /etc/default/tomcat7
3번째 문단에 JAVA_HOME이 주석처리 되어 있는데 주석을 풀고 자신의 JAVA 경로를 넣어주면 된다.
![](/RefImage/tomcat_2.JPG)

이제 설치와 설정은 끝났다.  
Tomcat을 구동시키기 위해 아래 명령어를 사용한다.  

	$sudo service tomcat7 start
Tomcat을 구동시키고 웹브라우저에서 http://(웹서버 ip주소):8080 으로 접속하면 It works! 라고 출력되는 페이지를 볼 수 있다.  
	
Tomcat을 중지시키기 위해서는 stop을 쓰면된다.  

	$sudo service tomcat7 stop

###3. Apache2 설치 및 Tomcat과 연동.  
Apache2와 Apache-Tomcat을 연동하는 패키지를 설치한다.  

	$sudo apt-get install apache2 libapache2-mod-jk
설치가 완료되면 Apache에서 jk module을 사용하게 하기 위한 설정을 해준다.  

	$sudo nano /etc/apache2/apache2.conf

아래 코드를 추가한다.  

	#JK_MODULE
    LoadModule jk_module /usr/lib/apache2/modules/mod_jk.so
    
    #ServerName
    ServerName localhost
다음으로 jk module을 이용해서 Apache가 Tomcat으로 넘길 패턴을 설정한다.  

	$sudo nano /etc/apache2/sites-enabled/000-default
아래 그림에서 처럼 JkMount부분을 추가한다. 무조건 따라서 복사 하는 것은 아니고 원하는 확장자를 넣어주면 된다.  

	JkMount /*.jsp ajp13_worker
	JkMount /*.gm ajp13_worker
![](/RefImage/apache_1.JPG)

이제 apache를 재시작 해주면 될...거라 생각했는데 안됐다.  
503에러가 발생했는데 원인과 해결법을 계속 찾아 해매다가 찾았다.  
(너무 고마운 문제해결을 도와준 사이트 : http://thetechnocratnotebook.blogspot.kr/2012/05/installing-tomcat-7-and-apache2-with.html)  

아래 한 작업까지 해주면 완성이다.  

	$sudo nano /etc/tomcat7/server.xml
에 들어가서 아래의 줄을 찾아서 주석을 지워준다.

	<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
이제 Tomcat과 Apache를 재시작 해주면 된다.  

	$sudo service tomcat7 restart
    $sudo service apache2 restart
이제 웹브라우저에서 tomcat에 있는 페이지에 접근할때 번거롭게 8080포트를 써줄 필요 없이 바로 ip주소/jsp파일이름 으로 접근할 수 있다.
