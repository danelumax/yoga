package com.dynamicProxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class MyInterceptor implements InvocationHandler{

	private Object target;
	private Transaction transaction;
	
	public MyInterceptor(Object target, Transaction transaction) {
		super();
		this.target = target;
		this.transaction = transaction;
	}
	
	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
		
		String methodName = method.getName();
		
		if("savePerson".equals(methodName) || "updatePerson".equals(methodName)
				|| "deletePerson".equals(methodName)) {
			this.transaction.beginTransaction(); //开启事务
			method.invoke(target); //调用目标的方法
			this.transaction.commit(); //事务的提交
		} else {
			method.invoke(target);
		}
		
		return null;
	}

}
