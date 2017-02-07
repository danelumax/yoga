<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>title</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
	
  </head>
  
  <body>
    <table border="1" width="438">
    	<tr>
    		<th>编号</th>
    		<th>名称</th>
    		<th>单价</th>
    	</tr>
    	<c:forEach items="${products}" var="p" varStatus="vs">
    		<tr class="${vs.index%2==0?'odd':'even' }">
	    		<td>${p.id}</td>
	    		<td>${p.name}</td>
	    		<td>${p.price}</td>
	    	</tr>
    	</c:forEach>
    </table>
  </body>
</html>
