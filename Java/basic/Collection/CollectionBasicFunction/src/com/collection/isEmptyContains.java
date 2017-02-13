package com.collection;

import java.util.ArrayList;
import java.util.Collection;

/*
判断
	isEmpty() 
	contains(Object o) 
	containsAll(Collection<?> c)
*/

class Person{
	
	int id; 
	
	String name;

	public Person(int id, String name) {
		this.id = id;
		this.name = name;
	}

	@Override
	public String toString() {
		return "{编号："+this.id+" 姓名："+ this.name+"}";
	}
	
	@Override
	public boolean equals(Object obj) {
		Person p = (Person)obj;
		return this.id == p.id ;
	}
	
	
	//java规范： 一般重写equlas方法我们都会重写hashCode方法的。
	@Override
	public int hashCode() {
		return this.id;
	}
	
	
	
}


class Dog{}


public class isEmptyContains {
	
	public static void main(String[] args) {
		/*Collection c = new ArrayList();
		c.add("令计划");
		c.add("徐才厚");
		c.add("周永康");
		System.out.println("判断集合是否为空元素："+ c.isEmpty());
		System.out.println("判断集合中是否存在指定的元素："+ c.contains("薄熙来"));*/
		
		//集合添加自定义的元素
		Collection c = new ArrayList();
		c.add(new Person(110,"狗娃"));
		c.add(new Person(119,"狗剩"));
		c.add(new Person(120,"铁蛋"));
		
		
		Collection c2 = new ArrayList();
		c2.add(new Person(110,"狗娃"));
		c2.add(new Person(119,"狗剩"));
		c2.add(new Person(104,"陈狗剩"));
		
		
		System.out.println("c集合有包含c2集合中的所有元素吗？"+ c.containsAll(c2));
		
		
		//如果在现实生活中，只要身份证编号一致，那么就为同一个人。
		System.out.println("存在该元素吗？"+c.contains(new Person(120,"陈铁蛋"))); // 其实contains方法内部是依赖于equals方法进行比较的。
		System.out.println("集合的元素："+ c);
		
		
	}
}
