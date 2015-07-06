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
|           1           |         3         |         VDD        |    3.3V   |
|           -           |         4         | NC (Not Connected) |     -     |
|           -           |         5         | NC (Not Connected) |           |
|           3           |         6         |         SCL        |    SCL    |
