package com.hibernate.test.api;

import java.util.List;

import org.hibernate.Query;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.classic.Session;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
//详解Query对象
public class Query_test {
	@Test
	//Query对象 封装HQL语句的对象
	//Query中封装查询细节api
	public void fun1(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		
		Query query = session.createQuery("from com.hibernate.test.helloworld.User");
		
		//分页 limit index,count;
		
		//指定结果从第几个开始拿 (index)
		query.setFirstResult(0);
		//指定拿几个结果 (count)
		query.setMaxResults(2);
		
		//query.list() 将hql语句执行,并返回结果(多行)
		List<User> list =  query.list();
		System.out.println(list);
		//uniqueResult 将hql语句执行,并返回结果(一行)
		//User u = (User) query.uniqueResult();
		//System.out.println(u);
		//---------------------------------------------------------
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
	}
}
