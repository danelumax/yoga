<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>显示所有的商品:JSON</title>
    
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
							var text = xhr.responseText;//文本
							var products = eval("("+text+")");//把文本转成JSON
							document.getElementById("d1").innerHTML="<table id='t1' border='1' width='438'><tr><th>编号</th><th>名称</th><th>价格</th></tr></table>";
							for(var i=0;i<products.length;i++){
								var p = products[i];
								var tableObj = document.getElementById("t1");
								//得到表格对象:HTML DOM
								//调用insertRow插入一行，返回TableRow
								var trObj = tableObj.insertRow(tableObj.rows.length);
								//TableRow的insertCell，返回TableCell
								var idTdObj = trObj.insertCell(trObj.cells.length);
								idTdObj.innerHTML=p.id;
								var nameTdObj = trObj.insertCell(trObj.cells.length);
								nameTdObj.innerHTML=p.name;
								var pricieTdObj = trObj.insertCell(trObj.cells.length);
								pricieTdObj.innerHTML=p.price;
												
							}
						
						}
					}
				}
				xhr.open("GET","${pageContext.request.contextPath}/servlet/ServletDemo5?time="+new Date().getTime());
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
