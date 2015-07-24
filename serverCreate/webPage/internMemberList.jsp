<%@ page language="java" contentType="text/html; charset=EUC-KR" pageEncoding="EUC-KR" %>
<%@ page import = "java.sql.*" %>

<%
	//���� ����Ʈ : http://hyeonstorage.tistory.com/112
	Connection conn = null;				//Connection ��ü�� null�� �ʱ�ȭ
	PreparedStatement pstmt = null;

	try{
		String url = "jdbc:mysql://localhost:3306/internMember";		//����Ϸ��� DB���� ������ URL
		String id = "root";												//����� ����
		String pw = "tinyos";											//����� ������ ��й�ȣ

		Class.forName("com.mysql.jdbc.Driver");							//Mysql ����̹� �ε�. DriverManager�� ��ϵ�. ���α׷� ����� �ѹ��� �ʿ�.
		conn = DriverManager.getConnection(url, id, pw);				//DriverManager ��ü�κ��� Connection ��ü�� ���´�.
		out.println("Database�� ����Ǿ����ϴ�.");						//���� ������ �޼��� ���
	
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
			<td colspan="3">2015 �ϰ� ���Ͻ� KETI ���</td>
		</tr>
		<tr align = "center" height = "30">
			<td>�̸�</td>
			<td>��ȣ</td>
			<td>�̸���</td>
		</tr>
<%
		String sql = "select * from memberInfo";
		pstmt = conn.prepareStatementt(sql);		//prepareStatement���� �ش� sql�� �̸� �������Ѵ�.

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
	}finally{ //���� ���� ������ ������� ����� �ڿ����� ������ ����Ѵ�. �̶� ���� ������ �߿��Ѵ�.
		if(rs != null) try{rs.close();}catch(SQLException sqle){}		//ResultSet ��ü ����
		if(pstmt != null) try{pstmt.close();}catch(SQLException sqle){}	//PreparedStatement ��ü ����
		if(conn != null) try{conn.close();}catch(SQLException sqle){}	//Connection ��ü ���� 
%>
		</table>
	</body>
</html>