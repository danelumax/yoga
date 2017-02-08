<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>原型</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->

  </head>
  
  <body>
    <script type="text/javascript">
    	//相当于在原来的String源码上添加了一个trim()方法
    	String.prototype.trim = function(){
			return this.replace(/(^\s*)|(\s*$)/g, "");
		}
    	var s1 = "        abc           ";
    	alert("|"+s1+"|");
    	alert("|"+s1.trim()+"|");
    </script>
  </body>
</html>
