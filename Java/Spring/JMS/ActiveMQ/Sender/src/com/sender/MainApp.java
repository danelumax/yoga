package com.sender;

import javax.jms.Queue;

import org.apache.activemq.command.ActiveMQQueue;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {

	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		JmsMessageSender jmsMessageSender = (JmsMessageSender)context.getBean("jmsMessageSender"); //use @Service
		
		/* send to default destination */ 
		jmsMessageSender.send("Hello JMS");
		
		/* send to a message specified destination */
		Queue queue = new ActiveMQQueue("Ericsson");
		jmsMessageSender.send(queue, "Hello Ericsson Message");
		
		((ClassPathXmlApplicationContext)context).close();
	}

}
