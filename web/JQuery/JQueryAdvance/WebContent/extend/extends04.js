/*
 * ***** 例子介绍： ***** 
 * 写一个函数，该函数的名称是extend,有两个参数：destination,source
   1、需求： 如果destination和source都是json对象，完成从source到destination的复制
     意义： 用两组独立的json对象，共同构建一个新类， 如果在destination 和 source中，某个成员重复了， 使用source的数据。
     
   2、如果destination是一个函数，source是一个json对象，则把source中的每一个key,value对赋值给destination的prototype
   	 意义： 用source的json对象，派生destination类。
     
   3、如果destination,source都是函数，则把source的prototype中的内容赋值给destination的prototype
     意义： 用两组独立的function对象，共同构建一个新类， 如果在destination 和 source中，某个成员重复了， 使用source的数据。
 */
namespace("com.jquery");
com.jquery.extend = function(destination,source){
	if(typeof destination == "object"){//destination是一个json对象
		if(typeof source == "object"){//source是一个json对象
		    //把source中的每一个key,value值赋值给destination
			for(var i in source){
				destination[i] = source[i];
			}
		}
	}
	
	if(typeof destination == "function"){
		if(typeof source == "object"){
			for(var i in source){
				destination.prototype[i] = source[i];
			}
		}
		if(typeof source == "function"){
			destination.prototype = source.prototype;
		}
	}
	return destination;
}

var destination = com.jquery.extend({
	cc:'cc'
},{
	aa:'aa',
	bb:'bb'
});

alert(destination.aa);

function Person(){
	
}
com.jquery.extend(Person,{
	aa:'aa'
});
