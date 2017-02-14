/**
 * 该函数是一个对象,该对象是由Function产生的
 */
function Person(){
	
}
alert(Person.constructor);

Person.a = 5;//给Person对象添加了一个属性为a,值为5

function Student(){
	
}

Person.b = Student;//给Person对象添加了一个属性为b,值为Student的对象

var json = {
	aa:'aa'
};

Person.c = json;//给Person对象天界另一个属性为c,值为json对象

alert(Person.c.aa);

/**
 * A.B.C.D.E.F.G.H()
 */
function A(){
	
}
function b(){
	
}
function c(){
	
}
function d(){
	
}
function e(){
	
}
function f(){
	
}
function g(){
	
}
function h(){
	alert("hh");
}
A.B = b;
A.B.C = c;
A.B.C.D = d;
A.B.C.D.E = e;
A.B.C.D.E.F = f;
A.B.C.D.E.F.G = g;
A.B.C.D.E.F.G.H = h;
A.B.C.D.E.F.G.H();//A.B.C.D.E.F.G是命名空间

var AA = {};
AA.BB = b;
AA.BB.CC = c;
AA.BB.CC.DD = d;
AA.BB.CC.DD.EE = e;
AA.BB.CC.DD.EE.FF = f;
AA.BB.CC.DD.EE.FF.GG = g;
AA.BB.CC.DD.EE.FF.GG.HH = h;
AA.BB.CC.DD.EE.FF.GG.HH();

/**
 * a.b.c.d.e.f
 */
function namespace(namespaceString){
	var temp = [];//声明了一个空的数组
	var array = namespaceString.split(".");
	for(var i=0;i<array.length;i++){
		temp.push(array[i]);
		/**
		 * 把多个json对象添加了window上
		 */
		eval("window."+temp.join(".")+"={}");
		//把多个function添加到了window上
		//eval("window."+temp.join(".")+"=function(){}");
	}
}
/**
 * 把com.itheima12动态的添加到了window对象上
 */
var tempnamespace = namespace("com.itheima12");
alert(window);
