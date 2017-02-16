package com.activemq.topic;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;

@Service
public class TopicReceiver {
	@Autowired
	private JmsTemplate jt = null;

	public static void main(String[] args) throws Exception {
		ApplicationContext ctx = new ClassPathXmlApplicationContext("spring-topic.xml");
		TopicReceiver ct = (TopicReceiver) ctx.getBean("topicReceiver");
		
		String msg = (String) ct.jt.receiveAndConvert();
		
		System.out.println("Receive msg: " + msg);		
	}
}
