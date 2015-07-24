<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR" %>
<%@ page import = "java.sql.*" %>

<%
	//참고 사이트 : http://hyeonstorage.tistory.com/112
	Connection conn = null;				//Connection 객체를 null로 초기화
	PreparedStatement pstmt = null;

	try{
		String url = "jdbc:mysql://localhost:3306/internMember";		//사용하려는 DB명을 포함한 URL
		String id = "root";												//사용자 계정
		String pw = "tinyos";											//사용자 계정의 비밀번호

		Class.forName("com.mysql.jdbc.Driver");							//Mysql 드라이버 로딩. DriverManager에 등록됨. 프로그램 수행시 한번만 필요.
		conn = DriverManager.getConnection(url, id, pw);				//DriverManager 객체로부터 Connection 객체를 얻어온다.
		out.println("Database와 연결되었습니다.");						//연결 성공시 메세지 출력
	
%>
<html>
	<title>
	JSP practice - pcm
	</title>
	<head>
	</head>
	
	<body>
		<table border = "1" width = "900" align = "center">
		<tr align = "center" height = "50">
			<td colspan="3">2015 하계 인턴십 KETI 멤버</td>
		</tr>
		<tr align = "center" height = "30">
			<td>이름</td>
			<td>번호</td>
			<td>이메일</td>
		</tr>
<%
		String sql = "select * from memberInfo";
		pstmt = conn.prepareStatementt(sql);		//prepareStatement에서 해당 sql을 미리 컴파일한다.

		ResultSet rs = pstmt.executeQuery();

		while(rs.next()){
			String name = rs.getString("m_name");
			String phone = rs.getString("m_phone");
			String email = rs.getString("m_email");
%>
		<tr align = "center">
			<td><%=name%></td>
			<td><%=phone%></td>
			<td><%=email%></td>
		</tr>

<%	
		}
	}catch(Exception e){
		e.printStackTrace();
	}finally{ //쿼리 성공 유무에 상관없이 사용한 자원들을 해제해 줘야한다. 이때 해제 순서가 중요한다.
		if(rs != null) try{rs.close();}catch(SQLException sqle){}		//ResultSet 객체 해제
		if(pstmt != null) try{pstmt.close();}catch(SQLException sqle){}	//PreparedStatement 객체 해제
		if(conn != null) try{conn.close();}catch(SQLException sqle){}	//Connection 객체 해제 
%>
		</table>
	</body>
</html>