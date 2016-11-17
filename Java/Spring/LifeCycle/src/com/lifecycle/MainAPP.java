package com.lifecycle;

import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainAPP {

	public static void main(String[] args) {
		AbstractApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		LifeCycleTest obj = (LifeCycleTest) context.getBean("lifeCycleTest");
		obj.getMessage();
		/* no web application */
		context.registerShutdownHook();
	}

}
