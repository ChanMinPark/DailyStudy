(Tip. MarkDown 표 편리하게 작성해주는 사이트 http://www.tablesgenerator.com/markdown_tables)

#**>>라즈베리파이에 LCD 연결시키기**  
####1. LCD pin과 라즈베리파이 GPIO의 결선  
(lcd_connect.py 기준)  

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

![]()  
