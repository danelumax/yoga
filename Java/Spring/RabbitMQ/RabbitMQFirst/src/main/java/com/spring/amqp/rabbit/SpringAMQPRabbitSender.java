package com.spring.amqp.rabbit;

import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SpringAMQPRabbitSender {
    
    public static void main(String[] args) throws Exception {
    	ApplicationContext context = new ClassPathXmlApplicationContext("Beans-sender.xml");
    	AmqpTemplate amqpTemplate = (AmqpTemplate)context.getBean("amqpTemplate");
    	
    	int messagCount = 0;
    	while (messagCount < 10){
    		amqpTemplate.convertAndSend("liwei.first", "Message : Hello Rabbit " + messagCount++);
    	}
	 	System.out.println( messagCount + " message(s) sent successfully.");
	}
}