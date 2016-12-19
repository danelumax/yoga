<%@taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
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

<h2>Please Insert Rent Information</h2>
<form:form method="POST" action="/RegistrationWeb/insertRentInfo">
   <table>
    <tr>
        <td><form:label path="hostName">HostName</form:label></td>
        <td><form:input path="hostName" /></td>
    </tr>
    <tr>
        <td><form:label path="eid">eid</form:label></td>
        <td><form:input path="eid" /></td>
    </tr>
    <tr>
        <td><form:label path="duration">Duration</form:label></td>
        <td><form:input path="duration" /></td>
    </tr>
    <tr>
        <td colspan="2">
            <input type="submit" value="Submit"/>
        </td>
    </tr>
</table>  
</form:form>
</body>
</html>