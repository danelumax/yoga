/*
 * ***** 例子介绍： ***** 
 * 1. 用一个json对象的数据， 为空类Person添加成员变量
 * 2. 一个类的内部结构，由json对象和extend方法进行封装
 * 3. 用namespace，将extend方法进行区分
 */

/**
 * 在extend函数内部定义了一个函数，把传递进来的json对象的每一个key,value值动态的添加到了
 * 内部函数的prototype中
 * @param {Object} json
 */


namespace("com.jquery");
com.jquery.extend = function (json){
	/**
	 * 声明了一个函数
	 */
	function F(){
		
	}
	/**
	 * 遍历json对象中的每一个key,value值，把每一个key,value值赋值给F.prototype
	 */
	for(var i in json){
		F.prototype[i] = json[i];
	}
	return F;//F就是一个对象
}

//var Person = extend({
//	aa:'aa',
//	bb:'bb'
//});
//用json添加到F的prototype中，封装出一个类
var Person = com.jquery.extend({
	aa:'aa',
	bb:'bb'
});
var p = new Person();
alert(p.aa);
