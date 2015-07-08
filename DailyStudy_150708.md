##1. I2C에 대한 설명이 잘 되어 있는 사이트  
http://naito.tistory.com/entry/%EB%A6%AC%EB%88%85%EC%8A%A4%EC%99%80-I2C  
  
##2. RaspberryPi의 UART(ttaAMA0)통신에 대한 설명 사이트(ttaAMA0를 사용하기 위한 전처리)  
http://lifeseed.tistory.com/m/post/94  
  
라즈베리파이의 UART는 ttyAMA0를 통해 제어된다.  
그런데, ttyAMA0는 부팅시 설정되어 사용되어서 Port Open이 안된다. 그래서 ttyAMA0를 사용하기 위해서는 먼저 Free 상태로 만들어주는 작업이 필요하다.  
(1) /boot/cmdline.txt 수정  
    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait  
(BerePi의 cmdline.txt를 확인해보니 맨 뒤에 ip=169.254.0.2 까지 붙여져 있다.)  
  
(2) /etc/inittab 수정  
72 line ttyAMA0 가 있는 라인 주석처리  
   #Spawn a getty on Raspberry Pi serial line
   #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

(3) 재부팅  
  
##3. Python의 logging 모듈에 대해 설명이 잘 되어 있는 사이트  
http://gyus.me/?p=418  
  

 
