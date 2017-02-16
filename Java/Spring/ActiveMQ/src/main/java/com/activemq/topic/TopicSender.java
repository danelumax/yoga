package com.activemq.topic;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.Session;
import javax.jms.TextMessage;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.jms.core.MessageCreator;
import org.springframework.stereotype.Service;

@Service
public class TopicSender {
	@Autowired
	private JmsTemplate jt = null;
	
	public static void main(String[] args)throws Exception {
		ApplicationContext ctx = new ClassPathXmlApplicationContext("spring-topic.xml");
		TopicSender ct = (TopicSender)ctx.getBean("topicSender");
		ct.jt.send(new MessageCreator() {
			public Message createMessage(Session s) throws JMSException {
				TextMessage msg = s.createTextMessage("ActiveMQ Topic First Test !!!");
				return msg;
			}
		});
	}
}
