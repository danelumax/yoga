package com.activemq.listener;

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
public class QueueSender {
	@Autowired
	private JmsTemplate jt = null;
	
	public static void main(String[] args)throws Exception {
		ApplicationContext ctx = new ClassPathXmlApplicationContext("spring-listener.xml");
		QueueSender ct = (QueueSender)ctx.getBean("queueSender");
		ct.jt.send(new MessageCreator() {
			public Message createMessage(Session s) throws JMSException {
				TextMessage msg = s.createTextMessage("ActiveMQ Queue First Test !!!");
				return msg;
			}
		});
	}

}
