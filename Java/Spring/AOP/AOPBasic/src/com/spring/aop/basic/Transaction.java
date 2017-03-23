package com.spring.aop.basic;


//切面
public class Transaction {
	public void beginTransaction(){
		System.out.println("begin transaction");
	}
	
	public void commit(){
		System.out.println("commit");
	}
}
