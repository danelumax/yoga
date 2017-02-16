package com.activemq.topic.persistent;


import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

public class ConsumerMessageListener implements MessageListener {

	public void onMessage(Message message) {
		System.out.println("topic 收到消息:"+message);  
	}  

}  
