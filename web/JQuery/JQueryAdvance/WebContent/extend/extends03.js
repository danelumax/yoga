/*
 * ***** 例子介绍： ***** 
 * 1. json对象和extend方法封装新类Person
 * 2. 再用另一个json对类Person，进行派生（进行继承），构建新类SuperPerson
 */


/**
 * 写一个命名空间com.jquery,在该命名空间下有一个方法extend
 * 该方法有两个参数json,prop
 *   该方法会调用两次，
 *   第一次传递一个参数，该参数是json对象
 *   第二次传递两个参数，第一个参数是function,第二个参数是prop
 */
namespace("com.jquery");
/**
 * 创建出来一个Person函数
 */
com.jquery.extend = function(json,prop){
	function F(){
		
	}
	/**
	 * 第一次调用extend方法
	 */
	if (typeof json == "object") {//json参数是一个json对象
		for(var i in json){//把json对象中的每一个key,value赋值给F的prototype
			F.prototype[i] = json[i];
		}
	}
	
	/**
	 * 第二次调用extend方法
	 */
	if(typeof json == "function"){
		/**
		 * 让F的prototype指向json的prototype
		 */
		F.prototype = json.prototype;
		/**
		 * 再把prop的每一个key,value值赋值给F的prototype
		 */
		for(var j in prop){
			F.prototype[j] = prop[j];
		}
	}
	return F;
}


var Person = com.jquery.extend({
	aa:'aa',
	bb:'bb'
});
var p = new Person();
alert(p.aa);

var SuperPerson = com.jquery.extend(Person,{
	cc:'cc'
});
var sp = new SuperPerson();
alert(sp.cc);
