function ajaxFunction(){
	   var xmlHttp;
	   try{ // Firefox, Opera 8.0+, Safari
	        xmlHttp=new XMLHttpRequest();
	    }
	    catch (e){
		   try{// Internet Explorer
		         xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
		      }
		    catch (e){
		      try{
		         xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
		      }
		      catch (e){}
		      }
	    }
	
		return xmlHttp;
	 }

window.onload=function(){
//	ajax("../AjaxServlet","post",null,function(data){//data为回调函数的形参
//		alert(data);
//	});
	ajax2({
		url:'../AjaxServlet',
		method:'post',
		data:null,
		callback:function(data){
			/**
			 * ajaxJSON.callback(xmlHttp.responseText);//xmlHttp.responseText为回调函数的实参
			 * 这里的this代表this所在的json对象
			 * ajaxJSON.callback.call(window,xmlHttp.responseText);//xmlHttp.responseText为回调函数的实参
			 * 这里的this代表window
			 */
			alert(this);
		}
	});
}

function ajax(url,method,data,callback){
	//获取xmphttpRquest对象
	var xmlHttp=ajaxFunction();
	//事件处理程序
		xmlHttp.onreadystatechange=function(){
			//alert(xmlHttp.readyState);
			//alert(xmlHttp.status)
			if(xmlHttp.readyState==4){
				if(xmlHttp.status==200||xmlHttp.status==304){
					callback(xmlHttp.responseText);//xmlHttp.responseText为回调函数的实参
				}
			}
	  }	
	//打开连接
	xmlHttp.open(method,url,true);
	//设置响应头
	xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	//发送请求
	xmlHttp.send("data="+data);
}

function ajax2(ajaxJSON){
	//获取xmphttpRquest对象
	var xmlHttp=ajaxFunction();
	//事件处理程序
		xmlHttp.onreadystatechange=function(){
			//alert(xmlHttp.readyState);
			//alert(xmlHttp.status)
			if(xmlHttp.readyState==4){
				if(xmlHttp.status==200||xmlHttp.status==304){
					ajaxJSON.callback.call(window,xmlHttp.responseText);//xmlHttp.responseText为回调函数的实参
				}
			}
	  }	
	//打开连接
	xmlHttp.open(ajaxJSON.method,ajaxJSON.url,true);
	//设置响应头
	xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	//发送请求
	xmlHttp.send("data="+ajaxJSON.data);
}
