package com.thread;

public class DrawTest {

	public static void main(String[] args) {
		Account acct = new Account("1234567", 0);
		
		DrawThread draw = new DrawThread(acct, 800);
		DepositThread depositA = new DepositThread(acct, 800);
		DepositThread depositB = new DepositThread(acct, 800);
		DepositThread depositC = new DepositThread(acct, 800);
		
		new Thread(draw, "Thread Drawer").start();
		new Thread(depositA, "Thread depositA").start();
		new Thread(depositB, "Thread depositB").start();
		new Thread(depositC, "Thread depositC").start();
	}

}
