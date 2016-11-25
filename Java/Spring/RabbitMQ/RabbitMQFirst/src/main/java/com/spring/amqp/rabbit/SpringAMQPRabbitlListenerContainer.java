package com.spring.amqp.rabbit;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SpringAMQPRabbitlListenerContainer {
	public static void main(String[] args) {
        /* Initialize Spring IOC Container */
		new ClassPathXmlApplicationContext("Beans-listener.xml");
	}
}