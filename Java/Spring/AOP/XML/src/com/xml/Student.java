package com.xml;

public class Student {
	private Integer age;
	private String name;
	public void setAge(Integer age) {
		this.age = age;
	}
	public Integer getAge() {
	    System.out.println("Age : " + this.age );
	    return this.age;
	}
	
	public void setName(String name) {
	    this.name = name;
	}
	public String getName() {
	    System.out.println("Name : " + this.name );
	    return this.name;
	} 
	
	public void printThrowException() {
	    System.out.println("Exception raised ...");
	    throw new IllegalArgumentException();
	}
}
