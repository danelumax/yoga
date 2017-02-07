<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>显示所有的商品</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">
	<script type="text/javascript" src="${pageContext.request.contextPath}/util.js"></script>
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
	<style type="text/css">
		.odd{
			background-color: #c3f3c3;
		}
		.even{
			background-color: #f3c3f3;
		}
	</style>
	<script type="text/javascript">
		window.onload=function(){
			document.getElementById("bt1").onclick=function(){
				//发出异步请求
				var xhr = getXHR();
				xhr.onreadystatechange=function(){
					if(xhr.readyState==4){
						if(xhr.status==200){
							document.getElementById("d1").innerHTML=xhr.responseText;//  text/*
						}
					}
				}
				xhr.open("GET","${pageContext.request.contextPath}/servlet/ServletDemo3?time="+new Date().getTime());
				xhr.send(null);
			}
		}
	</script>
  </head>
  
  <body>
    <input type="button" id="bt1" value="显示商品"/>
    <hr/>
    <div id="d1"></div>
  </body>
</html>
