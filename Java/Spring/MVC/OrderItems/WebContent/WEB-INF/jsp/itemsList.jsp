<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt"  prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Query Item List</title>
</head>
<body> 
<form action="queryItems" method="post">
Query Condition：
<table width="100%" border=1>
<tr>
<td><input type="submit" value="Query"/></td>
</tr>
</table>

Item List：
<table width="100%" border=1>
<tr>
	<td>Name</td>
	<td>Price</td>
	<td>Product Date</td>
	<td>Description</td>
	<td>Operation</td>
</tr>

<c:forEach items="${itemsList }" var="item">
<tr>
	<td>${item.name }</td>
	<td>${item.price }</td>
	<td><fmt:formatDate value="${item.createtime}" pattern="yyyy-MM-dd HH:mm:ss"/></td>
	<td>${item.detail }</td>
	
	<td><a href="editItem">Modify</a></td>
</tr>
</c:forEach>

</table>
</form>
</body>

</html>