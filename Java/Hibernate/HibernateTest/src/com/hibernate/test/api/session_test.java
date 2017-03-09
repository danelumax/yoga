package com.hibernate.test.api;

import java.util.List;

import org.hibernate.Criteria;
import org.hibernate.Query;
import org.hibernate.SQLQuery;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.classic.Session;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
//详解Session对象
public class session_test {
	@Test
	//Session对象 用于操作数据库
	//增
	public void fun1(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		
		User u = new User();
		u.setName("jerry");
		u.setPassword("1234");
		
		//调用Session的save方法保存对象到数据库中
		session.save(u);
		
		//关闭资源
		session.close();
		sf.close();
		
	}
	
	@Test
	//Session对象 用于操作数据库
	//改
	public void fun2(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//先查询出你要修改的对象
		User user = (User) session.get(User.class,5);
		
		//在查询结果上,进行修改
		user.setName("rose");

		session.update(user);
		
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
		
	}
	@Test
	//Session对象 用于操作数据库
	//删
	public void fun3(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		//先查询出你要修改的对象
				User user = (User) session.get(User.class,5);
				/*User user = new User();
				user.setId(1);*/
		//根据ID删除
		session.delete(user);
		
		//---------------------------------------------------------
		
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
		
	}
	@Test
	//Session对象 用于操作数据库
	//查询get
	public void fun4(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		//先查询出你要修改的对象
				User user = (User) session.get(User.class,6);
				
		//---------------------------------------------------------
		
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
		
		System.out.println(user);
	}
	@Test
	//Session对象 用于操作数据库
	//查询 load
	public void fun5(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		//先查询出你要修改的对象
				User user = (User) session.load(User.class,6);
				
		//---------------------------------------------------------
		
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
		
		System.out.println(user);
	}
	//get: get方法被调用时立刻  发送sql语句查询
	//load : 调用时并没有查询数据库,当我们需要使用该对象的时候,才查询数据
	//------------------------------------------------------------------------------------------------------------
	@Test
	//Session对象 用于操作数据库
	//查询所有User
	public void fun6(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		
		//HQL语言 => Hibernate Query Language
		//createQuery 传入hql语句查询
		//select * from t_user;
		Query query = session.createQuery("from com.hibernate.test.helloworld.User");
		//list 将语句执行,并返回结果
		List<User> list =  query.list();
		
		System.out.println(list);
		//---------------------------------------------------------
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
	}
	@Test
	//Session对象 用于操作数据库
	//查询所有User
	public void fun7(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
		//Criteria 查询 => Hibernate独创的面向对象的查询=> 无语句
		Criteria criteria = session.createCriteria(User.class);
		
		//select * from t_user;
		List<User> list =	criteria.list();
		
		System.out.println(list);
		//---------------------------------------------------------
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
	}
	
	@Test
	//Session对象 用于操作数据库
	//查询所有User
	public void fun8(){
		//1加载配置
		Configuration  conf = new Configuration().configure();
		//2 根据Configuration 配置信息创建 SessionFactory
		SessionFactory sf = conf.buildSessionFactory();
		//3 获得session
		Session session = sf.openSession();
		//打开事务
		Transaction ts = session.beginTransaction();
		
		//--------------------------------------------------------
			//原生的Sql查询
		SQLQuery query = session.createSQLQuery("select * from user");
		// addEntity 将查询结果封装到指定对象中
		query.addEntity(User.class);
		
		List<User> list = query.list();
		
		System.out.println(list);
		
		/*List<Object[]> list = query.list();
		
		for(Object[] objs : list){
			System.out.println(Arrays.toString(objs));
		}*/
		
		//---------------------------------------------------------
		//提交事务
		ts.commit();
		
		//关闭资源
		session.close();
		sf.close();
	}
//---------------------------------------------------------------------------
	/*
	 * session.save();
	 * session.update();
	 * session.delete();
	 * session.get();
	 * session.load(); 对比get
	 * session.createQuery()
	 * session.createCritieria();
	 * session.createSqlQuery();
	 * 
	 */
//-------------------------------------------------------------------
	//1 load方法.返回一个代理对象,获得其内容时,会查询数据库,是每次访问属性都会查询数据库吗?
	//答:不是每次都查.代理对象中有一个标识是否被初始化的boolean型变量. 记录是否被初始化过.
	//2 代理都是要基于接口的,用load方法返回的代理,就没有实现任何接口?
	//答: java中的动态代理是基于接口.  而 Hibernate 是使用javassist-3.12.0.GA.jar 产生代理对象的.
		// 该代理与被代理对象之间的关系是继承关系.与我们学的动态代理不是一种.所以不需要接口.
}
