<%@taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>  
<html>
	<head>
    	<title>Spring MVC Form Handling</title>
    	<style type="text/css">
		body {
			background-image: url('http://crunchify.com/bg.png');
		}
		</style>
	</head>

	<body>
		<h2>Current Rent Information</h2>
		<table border="1" width="400">
			<tr>
				<th>HostName</th>
				<th>eid</th>
				<th>Duration</th>
				<th>Start Time</th>
			</tr>
     		<c:forEach items="${list}" var="item">  
	  		<tr>          		
          		<td> <span class="HostName"><c:out value="${item.hostName}" /></span> </td>
          		<td> <span class="eid"><c:out value="${item.eid}" /></span> <br/> </td>
          		<td> <span class="Duration"><c:out value="${item.duration}" /></span> <br/>	</td>
          		<td> <span class="startTime"><c:out value="${item.startTime}" /></span> <br/>	</td>
      		</tr>
    		</c:forEach> 
		</table> 
		<h3>
			<a href="/RegistrationWeb/">Back to Home </a> <br>
		</h3> 
	</body>
</html>