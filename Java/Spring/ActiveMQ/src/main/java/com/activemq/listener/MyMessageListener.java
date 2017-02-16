package com.activemq.listener;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

public class MyMessageListener implements MessageListener {

	public void onMessage(Message msg) {
		TextMessage txtMsg = (TextMessage)msg;
		try {
			System.out.println("Trigger listener, receive message: " + txtMsg.getText());
		} catch (JMSException e) {
			e.printStackTrace();
		}
	}

}
