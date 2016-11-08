package com.helloworld;

public class HelloWorld {
	private String message;
	private int count;
	
	public void setMessage(String message) {
		this.message = message;
	}
	
	public void setCount(int count) {
		this.count = count;
	}
	
	public void getMessage() {
		System.out.println("Your Message = " + " " + this.message);
	}
	
	public void getCount() {
		this.count = this.count + 2;
		System.out.println("Your count = " + " " + this.count);
	}
}
