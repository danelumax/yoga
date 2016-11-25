package com.spring.nosql.redis;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

 
public class MainApp {
 
	public static void main(String[] args) {
		ApplicationContext applicationContext = new ClassPathXmlApplicationContext("Beans.xml");
		UserRepository userRepository = (UserRepository)applicationContext.getBean("userRepository");
		
		User user1 = new User("1", "user 1");
		User user2 = new User("2","user 2");
		User user3 = new User("Liwei","redis");
		
		userRepository.put(user1);
		userRepository.put(user2);
		userRepository.put(user3);
		
		System.out.println("Step 1 output : " + userRepository.getObjects());
		System.out.println("Step 2 output : " + userRepository.getObjects());
		
		System.out.println("After deleting user ...");
		userRepository.delete(user1);
		System.out.println("Step 3 output : " + userRepository.getObjects());
	}
}
