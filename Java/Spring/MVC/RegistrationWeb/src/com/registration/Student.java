package com.registration;

import java.io.Serializable;

public class Student implements Serializable {
	private Integer age;
	private String name;
	private Integer id;
	private String time;
	private String leaseTime;
   
	public Student() {
		this.name = "Default";
		this.age = 0;
		this.id = 0;
		this.time = null;
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
	public String getTime() {
		return time;
	}
	public void setTime(String time) {
		this.time = time;
	}
	public String getLeaseTime() {
		return leaseTime;
	}
	public void setLeaseTime(String leaseTime) {
		this.leaseTime = leaseTime;
	}
}