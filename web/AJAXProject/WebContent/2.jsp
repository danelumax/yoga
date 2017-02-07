<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>检测用户名是否可用</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">
	<script type="text/javascript" src="${pageContext.request.contextPath}/util.js"></script>
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
	<script type="text/javascript">
		window.onload=function(){
			document.getElementById("username").onblur=function(){
				if(this.value==""){
					alert("请输入用户名");
					this.focus();//恢复焦点
					return;
				}
				//发出异步请求
				var xhr = getXHR();
				xhr.onreadystatechange=function(){
					if(xhr.readyState==4){
						if(xhr.status==200){
							
							document.getElementById("msg").innerHTML=xhr.responseText;
							
						}
					}
				}
				/*
				xhr.open("GET","${pageContext.request.contextPath}/servlet/ServletDemo2?username="+this.value+"&time="+new Date().getTime());
				xhr.send(null);
				*/
				
				xhr.open("POST","${pageContext.request.contextPath}/servlet/ServletDemo2?time="+new Date().getTime());
				//设置请求消息头：告知客户端提交的正文的MIME类型
				xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
				xhr.send("username="+this.value);
			}
		}
	</script>
  </head>
  
  <body>
    <form action="" method="post">
    	用户名：<input type="text" id="username" name="username"/><span id="msg"></span><br/>
    	密码:<input type="password" id="password" name="password"/><br/>
    	<input type="submit" value="注册"/>
    </form>
  </body>
</html>
