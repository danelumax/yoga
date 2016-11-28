package com.thread;

public class Account {
	private String accountNo;
	private double balance;
	private boolean flag = false;
	
	public Account(String accountNo, double balance) {
		this.accountNo = accountNo;
		this.balance = balance;
	}
	
	public String getAccountNo() {
		return this.accountNo;
	}
	public void setAccountNo(String accountNo) {
		this.accountNo = accountNo;
	}
	public double getBalance() {
		return this.balance;
	}
	public void setBalance(double balance) {
		this.balance = balance;
	}
	public boolean isFlag() {
		return this.flag;
	}
	public void setFlag(boolean flag) {
		this.flag = flag;
	}
	
	public synchronized void draw(double drawAmount) {
		try {
			if (!flag) {
				wait();
			} else {
				System.out.println("<---" + Thread.currentThread().getName() + " draw money: " + drawAmount);
				this.balance -= drawAmount;
				flag = false;
				notifyAll();
			}
		} catch (InterruptedException ex) {
			ex.printStackTrace();
		}
	}
	
	public synchronized void deposit(double depositAmount) {
		try {
			if (flag) {
				wait();
			} else {
				System.out.println("--->" + Thread.currentThread().getName() + " deposit money: " + depositAmount);
				this.balance += depositAmount;
				flag = true;
				notifyAll();
			}
		} catch (InterruptedException ex) {
			ex.printStackTrace();
		}
	}
	
}
