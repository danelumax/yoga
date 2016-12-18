<%@ page contentType="text/html; charset=UTF-8" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>  
<html>
<head>
<title>Home Page</title>
<style type="text/css">
body {
	background-image: url('http://crunchify.com/bg.png');
}
</style>
</head>
<body>
	<br>
	<div style="text-align:center">
		<h2>
			---------- Welcome to Liwei's Page ----------<br> <br>
		</h2>
		<h3>
			<a href="student">Register Student's Information </a> <br>
			<a href="studentJSON ">Fetch JSON Info </a>
		</h3>
	</div>
	<br>
	<div style="text-align:center">
		<h2>Current Student Information</h2>
		<table border="1" width="400" align="center">
			<tr>
				<th>Name</th>
				<th>Age</th>
				<th>Id</th>
				<th>Lease Time</th>
			</tr>
     		<c:forEach items="${list}" var="item">  
	  		<tr>
	  			<td> <span class="Name"><c:out value="${item.name}" /></span> </td>
          		<td> <span class="Age"><c:out value="${item.age}" /></span> <br/> </td>
          		<td> <span class="id"><c:out value="${item.id}" /></span> <br/>	</td>
          		<td> <span class="id"><c:out value="${item.leaseTime}" /></span> <br/>	</td>
      		</tr>
    		</c:forEach> 
		</table>  
	</div>
</body>
</html>