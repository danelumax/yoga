package com.registration;
public class Student {
	private Integer age;
	private String name;
	private Integer id;
   
	public Student() {
		this.name = new Welcome().getName();
		this.age = 0;
		this.id = 0;
	}
   
	public void setAge(Integer age) {
		this.age = age;
	}
	public Integer getAge() {
		return age;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getName() {
		return name;
	}
	public void setId(Integer id) {
		this.id = id;
	}
	public Integer getId() {
		return id;
	}
}