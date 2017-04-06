package com.zhenti.observerPattern;

public class Reader implements Observer {

	private String name;
	
	public Reader(String name) {
		this.name = name;
	}
	
	@Override
	public void update(String msg) {
		System.out.println(name + " receive : " + msg);
	}

}
