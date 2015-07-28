#< Web2py 시작하기 >  

##1. Web2py 설치  
web2py 사이트에서 소스코드 다운로드 링크를 복사해서 wget으로 다운받는다.  

    $sudo wget http://www.web2py.com/examples/static/web2py_src.zip

##2. Web2py 실행  
리눅스용 web2py는 설치가 아니고 단지 압축만 풀어주면 된다.  

    $sudo unzip web2py_src.zip

압축이 풀린 폴더에 들어가서 web2py를 실행시킨다.

    $cd web2py  
    $sudo python web2py.py

##3. 원격 PC의 Web Browser에서 Web2py Admin Page 접속하기  
Web2py의 Admin Page는 로컬에서 접속하거나 Https를 통해서만 접근할 수 있다.  
그래서 다른 컴퓨터의 Web Browser를 통해서 Web2py의 웹서버에 있는 웹페이지는 접근이 되지만 Admin 페이지는 접근할 수 없어서 원격 PC에서 Web2py를 설정할 수 없다.  
이러한 문제를 해결하기 위해서 SSL 인증서를 Web2py 서버에 추가하는 방법을 사용한다.  
간단한 방법은 아래와 같다.(여기서 설명하는 방법은 개발할때만 사용하고 실제 상용될때는 사용하면 안된다.)  
  
(1) 이미 가지고 있는 인증서가 없다면 새로운 인증서를 만든다.(임의의 폴더에서 수행해도 무방하다.)

    $openssl genrsa -out server.key 2048
    $openssl req -new -key server.key -out server.csr
    $openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

두번째 명령을 수행할때 인증서에 들어갈 정보를 입력하라고 한다. 아래 사진과 같은 정보를 요구한다.  
![](/RefImage/web2py_ssl.jpg)

(2) 위의 과정을 수행하고 나면 3개의 파일이 생기는데 그중 server.key파일과 server.crt파일을 web2py의 루트폴더에 복사한다.  
  
(3) 그리고 web2py를 실행시킬 때 아래와 같이 실행한다.  

    $sudo python web2py.py -i (자신의 ip주소) -p 8000 -a '(원하는 비밀번호)' -c server.crt -k server.key

(4) 이제 아래와 같은 주소로 원격 PC의 Web Browser에서 웹페이지에 접근한다.(https 가 중요하다.)  

    https://(web2py 실행시 입력한 ip주소):8000
헌데 브라우저에서 인증서를 의심하여 접속을 막을 수 있다. 어차피 내가 만든 인증서이니 믿고 그냥 들어가도록한다.  
위 주소에서 Admin Page로 들어가면 정상적으로 들어가진다.  
