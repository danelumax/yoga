package com.activemq.topic.persistent;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

// 这是消费者代码，这里你可以创建 多个XMl文件，模拟多个消费者。  
public class JmsTopicReceiver{  
    public static void main(String[] args) throws Exception {  
        // 加载消费者监听  
        ApplicationContext context = new ClassPathXmlApplicationContext("spring-topic-persistent-subscriber.xml");  
        // 写个死循环，模拟服务器一直运行  
        while (true){}  
    }  
}  