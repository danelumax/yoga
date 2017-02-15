/*
 * 谁调用function， this就是谁
 */

/**
 * 任何一个对象都有可能成为任何一个对象的属性
 */
function Person(){
	alert(this);
}
Person();//window = this

function Student(){
	
}
Student.a = Person;
Student.a();//this就是Student
var json = {
	a:Person
}
json.a();//this就是json对象

//可以利用call和 apply函数改变this的指向
Person.call(json);//Person.call(json)==json.Person
Person.apply(Student);//Student.Person();


