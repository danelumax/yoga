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
			<a href="mainPage">Register Rent Information </a> <br>
			<a href="rentInfoJSON ">Fetch JSON Info </a>
		</h3>
	</div>
	<br>
	<div style="text-align:center">
		<h2>Current Rent Information</h2>
		<table border="1" width="500" align="center">
			<tr>
				<th>HostName</th>
				<th>eid</th>
				<th>Duration</th>
				<th>Lease Time</th>
			</tr>
     		<c:forEach items="${list}" var="item">  
	  		<tr>
	  			<td> <span class="HostName"><c:out value="${item.hostName}" /></span> </td>
          		<td> <span class="eid"><c:out value="${item.eid}" /></span> <br/> </td>
          		<td> <span class="Duration"><c:out value="${item.duration}" /></span> <br/>	</td>
          		<td> <span class="Leased Time"><c:out value="${item.leaseTime}" /></span> <br/>	</td>
      		</tr>
    		</c:forEach> 
		</table>  
	</div>
</body>
</html>