package com.thread;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Account {
	private final Lock lock = new ReentrantLock();
	private final Condition cond = lock.newCondition();
	
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
	
	public void draw(double drawAmount) {
		lock.lock();
		try {
			if (!flag) {
				cond.await();
			} else {
				System.out.println("<---" + Thread.currentThread().getName() + " draw money: " + drawAmount);
				this.balance -= drawAmount;
				flag = false;
				cond.signalAll();
			}
		} catch (InterruptedException ex) {
			ex.printStackTrace();
		} finally {
			lock.unlock();
		}
	}
	
	public void deposit(double depositAmount) {
		lock.lock();
		try {
			if (flag) {
				cond.await();
			} else {
				System.out.println("--->" + Thread.currentThread().getName() + " deposit money: " + depositAmount);
				this.balance += depositAmount;
				flag = true;
				cond.signalAll();
			}
		} catch (InterruptedException ex) {
			ex.printStackTrace();
		} finally {
			lock.unlock();
		}
	}
	
}
