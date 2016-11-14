package com.parent;

public class ParentTest {
	private String message1;
	private String message2;
	
	public void setMessage1(String message) {
		this.message1 = message;
	}
	public void setMessage2(String message) {
		this.message2 = message;
	}
	
	public void getMessage1() {
		System.out.println("Parent Message1 = " + " " + this.message1);
	}
	public void getMessage2() {
		System.out.println("Parent Message2 = " + " " + this.message2);
	}
}
