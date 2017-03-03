package com.hibernate.test.api;

import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import org.junit.Test;
//详解SessionFactory对象
public class sessionfactory_test {
	@Test
	//SessionFactory 创建session的工厂
	public void fun1(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		//3.1 openSession => 获得一个全新的Session对象
		sf.openSession();
		//3.2 getCurrentSession => 获得与当前线程绑定的session对象
		// 调用getCurrentSession 需要加上一个配置: <property name="hibernate.current_session_context_class">thread</property>
		sf.getCurrentSession();
		
	}
}
