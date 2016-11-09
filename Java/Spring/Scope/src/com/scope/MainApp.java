package com.scope;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {

	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		
		/* Default Scope */
		System.out.println("\nTest Default Scope is Singleton...");
		ScopeDefaultTest objA = (ScopeDefaultTest) context.getBean("scopeDefaultTest");
		objA.setMessage("I'm object A");
		System.out.println(objA + "\t" + objA.getMessage());
		
		ScopeDefaultTest objB = (ScopeDefaultTest) context.getBean("scopeDefaultTest");
		System.out.println(objB + "\t" + objB.getMessage());
		
		/* Singleton Scope */
		System.out.println("\nTest Singleton Scope ...");
		ScopeSingletonTest objC = (ScopeSingletonTest) context.getBean("scopeSingletonTest");
		objC.setMessage("I'm object C");
		System.out.println(objC + "\t" + objC.getMessage());
		
		ScopeSingletonTest objD = (ScopeSingletonTest) context.getBean("scopeSingletonTest");
		System.out.println(objD + "\t" + objD.getMessage());
		
		/* Prototype Scope */
		System.out.println("\nTest Prototype Scope ...");
		ScopePrototypeTest objE = (ScopePrototypeTest) context.getBean("scopePrototypeTest");
		objE.setMessage("I'm object E");
		System.out.println(objE + "\t" + objE.getMessage());
		
		ScopePrototypeTest objF = (ScopePrototypeTest) context.getBean("scopePrototypeTest");
		System.out.println(objF + "\t" + objF.getMessage());
	}

}
