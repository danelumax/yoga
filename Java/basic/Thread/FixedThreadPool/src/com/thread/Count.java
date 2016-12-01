package com.thread;

public class Count implements Runnable {
	private int i;
	
	public Count(int i) {
		this.i = i;
	}
	
	@Override
	public void run() {
		for(; this.i<100; this.i++) {
			System.out.println(Thread.currentThread().getName() + " i value is: " + this.i);
		}
	}
}
