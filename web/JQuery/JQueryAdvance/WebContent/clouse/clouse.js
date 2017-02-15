/*
 * 尝试提供public， private访问权限
 */

/**
 * 在函数内部定义的函数，在外部要使用
 *   闭包的一个使用场景：
 *      继承的封装
 *      匿名函数
 *          写4个函数setName,getName,aaa,bbb,让setName和getName成为公开的函数，让aaa,bbb成为私有的函数
 */
(function(window){
	function Person(){
		return {
			setName:setName,
			getName:getName
		};
	}
	/**
	 * 公开的函数
	 * @param {Object} name
	 */
	function setName(name){
		this.name = name;
	}
	function getName(){
		return this.name;
	}
	/**
	 * 私有函数
	 */
	function aaa(){
		
	}
	function bbb(){
		
	}
	//给window对象动态的添加了一个属性Person
	window.Person = Person;
})(window);

//window相当于一个全局public访问点
var Person = window.Person();
Person.setName("aaa");
alert(Person.getName());

