package com.scope;

public class ScopeDefaultTest {
	private String message;
	
	public void setMessage(String message) {
		this.message = message;
	}
	public String getMessage() {
		String result = "You Message : " + " " + this.message;
		return result;
	}
}
