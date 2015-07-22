#< 라즈베리파이에 Apache, Tomcat, Mysql 설치하기 >
###1. JAVA 확인하기.
Tomcat7이 apt에서 받을 수 있는 최신 버전인데 Tomcat7은 JAVA JDK 1.8에서 
동작하지 않는다.(컴파일이 되지 않는다.) 그래서 JAVA를 1.7로 
낮춰주어야한다. 먼저, JAVA 버전을 확인한다.
	$javac -version 버전이 1.8로 나오면 아래와 같은 과정으로 1.8을 
삭제하고 1.7로 새로 설치한다. JAVA를 apt로 설치하였을 경우에 아래 
명령어로 삭제 가능하다.
	$sudo apt-get purge oracle-java8-jdk purge는 설정까지 모두 
지우는 것이다. 설정을 남기려면 remove로 지우면 된다. 나는 oracle java가 
apt로 설치 되어 있었기 때문에 위와 같이 간단하게 지울 수 있었다. oracle 
java 7으로 설치하는 명령어는 아래와 같다.
	$sudo apt-get install oracle-java7-jdk 설치가 완료되고 
JAVA버전을 다시 확인해보면 1.7로 나온다. JAVA가 설치되면 환경설정을 
해준다. /etc/profile에 추가하거나 쉘에서만 추가해도 된다. Tomcat을 위한 
JAVA 환경설정은 Tomcat 설정파일에 다시 해 줄 것이다.
	$export JAVA_HOME=/usr/lib/jvm/jdk-7-oracle-armhf
###2. Tomcat7 설치하기.
(출처 : http://yoo7577.tistory.com/204) apt로 Tomcat7을 설치한다.
	$sudo apt-get install tomcat7 설치가 완료되면 설치 로그 맨 
아래를 잘 보아야한다. tomcat7이라는 user와 group이 새로 생긴다. 그리고, 
내 경우에는 JAVA_HOME이 제대로 잡히지 않아서 Tomcat7이 설치는 되었지만 
JAVA를 못 찾아서 구동은 바로 되지 못하였다. (사진 추가) Tomcat 구동시에 
이용하는 환경 설정 파일에 JAVA_HOME을 잡아주어야 한다.
	$sudo nano /etc/default/tomcat7 3번째 문단에 JAVA_HOME이 
주석처리 되어 있는데 주석을 풀고 자신의 JAVA 경로를 넣어주면 된다. (그림 
추가) 이제 설치와 설정은 끝났다. tomcat을 구동시키기 위해 아래 명령어를 
사용한다.
	$sudo service tomcat7 start tomcat을 중지시키기 위해서는 stop을 
쓰면된다.
	$sudo service tomcat7 stop
