package com.thread;

public class Volatile implements Runnable {

	volatile private boolean isRunning = true;
	
	public boolean isRunning() {
		return isRunning;
	}

	public void setRunning(boolean isRunning) {
		this.isRunning = isRunning;
	}

	@Override
	public void run() {
		System.out.println("Enter Thread ...");
		while(true == this.isRunning) {
		}
		System.out.println("Volatile isRunning == false\nisRunningThread has been canceled ...");
	}
}
