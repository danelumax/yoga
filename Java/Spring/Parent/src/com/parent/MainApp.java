package com.parent;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {

	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		
		ParentTest objA = (ParentTest)context.getBean("parentTest");
		objA.getMessage1();
		objA.getMessage2();
		
		SonTest objB = (SonTest)context.getBean("sonTest");
		objB.getMessage1(); /* Override */
		objB.getMessage2(); /* inherit */
		objB.getMessage3();
	}

}
