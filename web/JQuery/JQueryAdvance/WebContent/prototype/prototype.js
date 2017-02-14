function Person(){
	
}
//prototype 为某个函数对象添加模板属性，相当于类的成员函数或变量
alert(Person.prototype); //Person是一个函数对象，有一个默认的属性为prototype={},该特点在json对象中是不存在的

Person.prototype.aa = 5;//Person.prottype['aa'] = 5;

Person.prototype.bb = function(){
	alert("bb");
}
var p = new Person();
alert(p.aa);

var json = {};
alert(json.prototype);

/**
 * 模拟一个类，创建一个对象，设置属性，并进行输出
 */
function Student(){
	
}

//相当于为Student类添加一个成员函数，并且因为添加在prototype中，之后用Student new出来的新对象，都有这些成员函数
Student.prototype.setId = function(id){
	this.id = id;
}
Student.prototype.setName = function(name){
	this.name = name;
}
Student.prototype.getId = function(){
	return this.id;
}
Student.prototype.getName = function(){
	return this.name;
}

var s = new Student();
s.setId(4);
s.setName("王二麻子");
alert(s.getId());
alert(s.getName());

s.bb = 5;
alert(s.bb);

//Student的prototype没有添加过bb属性，所以新的对象bb为undefined
var ss = new Student();
alert("---------"+ss.bb);
