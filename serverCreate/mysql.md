##< Mysql 실습 >  
####1. Mysql 접속  

	(1) $mysql -u 사용자명 -p
	(2) $mysql -u root (계정과 비번을 만들지 않았을때)
	(3) $mysql -u root -p(루트 비번이 있을때)

####2. Database 보기 및 생성  
현재 생성되어 있는 Database들 확인하기  

	mysql>show databases;

Database 생성하기  

	mysql>create database DB명;

Database 선택  

	mysql>use DB명;

####3. DB 관리  
table 생성  

	mysql>create table 이름 (
    	-> 필드명 자료형,
    	-> 필드명 자료형
    	-> );

table 구조 보기  

	mysql>explain table이름;
	또는
	mysql>describe table이름;

새로운 레코드 추가하기

  mysql>insert into table이름 values ("값1", "값2", ... );
  또는
  mysql>insert into table이름 (field1, field2, ...) values ("값1", "값2", ... );

