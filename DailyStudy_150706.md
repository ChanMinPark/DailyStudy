#**>>라즈베리파이에 LCD, 온습도센서 연결시키기**  
####1. 개요  
라즈베리파이에 온습도센서를 연결하여서 온습도 정보를 LCD를 통해 출력하기

####2. LCD pin과 라즈베리파이 GPIO의 결선  

| LCD pin 	| Function            	| RasPi GPIO 	|
|---------	|---------------------	|------------	|
| 1       	| GND                 	| GND        	|
| 2       	| 5V                  	| 5V         	|
| 3       	| Contrast(0-5V)      	| GND        	|
| 4       	| RS(Register Select) 	| 6          	|
| 5       	| RW(Read Write)      	| GND        	|
| 6       	| E(Enable or Strobe) 	| 13         	|
| 7       	| Data 0              	| -          	|
| 8       	| Data 1              	| -          	|
| 9       	| Data 2              	| -          	|
| 10      	| Data 3              	| -          	|
| 11      	| Data 4              	| 19         	|
| 12      	| Data 5              	| 26         	|
| 13      	| Data 6              	| 21         	|
| 14      	| Data 7              	| 20         	|
| 15      	| 5V                  	| 5V         	|
| 16      	| -R/red              	| 16         	|
| 17      	| -G/green            	| 12         	|
| 18      	| -B/blue             	| 7          	|

####3. 라즈베리파이와 온습도 센서 결선
| 온습도 pin (with CO2) | 온습도 pin (only) |      Function      | RasPi pin |
|:---------------------:|:-----------------:|:------------------:|:---------:|
|           2           |         1         |         SDA        |    SDA    |
|           5           |         2         |         VSS        |    GND    |
|           1           |         3         | NC (Not Connected) |     -     |
|           -           |         4         | NC (Not Connected) |     -     |
|           1           |         5         |         VDD        |    3.3V   |
|           3           |         6         |         SCL        |    SCL    |

-Data Sheet(SHT20)  
http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Humidity_SHT20_Datasheet_V3.pdf

####4. 라즈베리파이에 SHT2x 셋팅하기  
(1) smbus package를 설치한다.  
$sudo apt-get install python-smbus  
$sudo apt-get install i2c-tools  
  
(2) Raspi-config에서 I2C를 enable해준다.
$sudo raspi-config  
-> 8. Advanced Options  
-> A7. I2C
-> (Yes)  
-> (Yes)  
  
(3) modules 파일을 수정한다.(아래 2줄을 추가한다.)  
i2c-bcm2708  
i2c-dev  
  
(4) 재부팅  
$sudo reboot  
