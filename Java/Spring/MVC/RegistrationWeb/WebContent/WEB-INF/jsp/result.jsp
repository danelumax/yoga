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
		<h2>Current Student Information</h2>
		<table border="1" width="300">
			<tr>
				<th>Name</th>
				<th>Age</th>
				<th>Id</th>
			</tr>
     		<c:forEach items="${list}" var="item">  
	  		<tr>
	  			<td> <span class="Name"><c:out value="${item.name}" /></span> </td>
          		<td> <span class="Age"><c:out value="${item.age}" /></span> <br/> </td>
          		<td> <span class="id"><c:out value="${item.id}" /></span> <br/>	</td>
      		</tr>
    		</c:forEach> 
		</table>  
	</body>
</html>