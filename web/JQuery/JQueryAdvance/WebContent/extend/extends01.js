/*
 * ***** 例子介绍： ***** 
 * 1. 为一个新类Student，封装访问器
 * 2. 新建一个类SuperStudent， 继承类Student， 同时继承类Student的成员方法
 */

function Student(){
	
}

//prototype相当于模板，相当于类的概念
Student.prototype.setName = function(name){
	this.name = name;
}
Student.prototype.getName = function(){
	return this.name;
}

function SuperStudent(){
	
}

SuperStudent.prototype = Student.prototype;
SuperStudent.prototype = new Student();
var superStudent = new SuperStudent();

superStudent.setName("aaa");
alert(superStudent.getName());

