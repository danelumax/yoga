package com.hibernate.test.api;

import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.classic.Session;
import org.junit.Test;
//详解Transaction对象
public class Transaction_test {
	@Test
	//Transaction 封装了事务的操作
	//开启事务
	//提交事务
	//回滚事务
	public void fun1(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//-------------------------------
		//打开事务
		Transaction ts = session.beginTransaction();
		//获得已经打开的事务对象(很少用)
		session.getTransaction();
		
		
		//Transaction 控制如何关闭事务
		//提交
		ts.commit();
		//回滚
		ts.rollback();
		
		
		//-------------------------------
		session.close();
		sf.close();
	}
	//事务的细节
	@Test
	public void fun2(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得与当前线程绑定的session
		Session session = sf.getCurrentSession();
		//-------------------------------
		//事务关闭时,会自动把与当前线程关联的session关闭,并删除
		session.beginTransaction().commit();
		
		//在获得当前线程绑定的session时. 获得的是新的session
		Session session2 = sf.getCurrentSession();
		
		System.out.println(session==session2);//false
		
		//-------------------------------
		session.close();
		sf.close();
	}
}
