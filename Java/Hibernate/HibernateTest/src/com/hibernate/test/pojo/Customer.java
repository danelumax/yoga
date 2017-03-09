package com.hibernate.test.pojo;

import java.util.HashSet;
import java.util.Set;

public class Customer {
	private Integer id;
	private String name;
	//在1 的一方,表达持有多的一方的引用=>使用集合
	private Set<Order> orders = new HashSet<Order>();
	
	private Integer version;
	
	
	public Customer(Integer id, String name) {
		super();
		this.id = id;
		this.name = name;
	}
	
	
	
	public Integer getVersion() {
		return version;
	}



	public void setVersion(Integer version) {
		this.version = version;
	}



	public Customer() {
	}


	public Integer getId() {
		return id;
	}
	public void setId(Integer id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public Set<Order> getOrders() {
		return orders;
	}
	public void setOrders(Set<Order> orders) {
		this.orders = orders;
	}
	@Override
	public String toString() {
		return "Customer [id=" + id + ", name=" + name + ", orders=" + orders
				+ "]";
	}
	
	
}
