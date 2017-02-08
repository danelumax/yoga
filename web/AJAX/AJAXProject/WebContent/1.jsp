<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>AJAX的编码步骤：测试异步交互是可行的</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
	<script type="text/javascript" src="${pageContext.request.contextPath}/util.js"></script>
	<script type="text/javascript">
		window.onload=function(){
			document.getElementById("bt1").onclick=function(){
				//发出异步请求：步骤
				
				//1、得到xhr（XMLHttpRequest）对象
				var xhr = getXHR();
				//2、注册状态变化监听器
				xhr.onreadystatechange=function(){
					//做出具体的处理
					if(xhr.readyState==4){
						if(xhr.status==200){
							alert("服务器已经响应结束了，去看看吧");
						}
					}
				}
				//3、建立与服务器的链接
				//如果访问的地址相同，浏览器就不会真正的发出请求
				xhr.open("GET","${pageContext.request.contextPath}/servlet/ServletDemo1?time="+new Date().getTime());
				//4、向服务器发出请求
				xhr.send(null);//没有正文
			}
		}
	</script>
  </head>
  
  <body>
    <input id="bt1" type="button" value="点我呀"/>
  </body>
</html>
