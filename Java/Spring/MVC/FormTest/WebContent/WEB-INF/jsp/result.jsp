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
		<h2>Submitted Student Information</h2>
		<table>
     <c:forEach items="${list}" var="item">  
	  <tr>
	  	<td>
          <span class="Name"><c:out value="${item.name}" /></span> <br/>
          <span class="Age"><c:out value="${item.age}" /></span> <br/>
          <span class="id"><c:out value="${item.id}" /></span> <br/>
        </td>
      </tr>
    </c:forEach> 
		</table>  
	</body>
</html>