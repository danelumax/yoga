package com.thread;

public class MainApp {

	public static void main(String[] args) throws InterruptedException {
			Volatile target = new Volatile();
			new Thread(target).start();
			Thread.sleep(1000);
			target.setRunning(false);
			System.out.println("Set false");
	}
}
