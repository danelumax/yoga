package com.hibernate.test.cache;

import java.util.List;

import org.hibernate.Session;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
import com.hibernate.test.utils.HibernateUtils;
//session缓存 的细节问题
public class Demo2 {
	@Test
	//1.保存对象时使用 save方法
	//  保存对象时使用 persist方法
	// 区别? 没有区别
	// persist(持久) 方法 来自于JPA 接口
	// save(保存) 方法来自于Hibernate
	public void fun1(){
		Session session = HibernateUtils.openSession();
		//session.beginTransaction();
		//------------------------------------------------
		User u = new User();
		u.setName("张三");
		
		//session.save(u); //insert语句被打印=> 目的:获得id
		session.persist(u); //
		//------------------------------------------------
		//session.getTransaction().commit();
		session.close(); // 游离状态
	}
	
	//2.1 HQL查询是否会使用一级缓存? HQL不会使用一级缓存.
	@Test
		public void fun2(){
			Session session = HibernateUtils.openSession();
			session.beginTransaction();
			//------------------------------------------------
			
			List<User> list1 = session.createQuery("from User").list();
			
			List<User> list2 = session.createQuery("from User").list();
			
			List<User> list3 = session.createQuery("from User").list();
			//------------------------------------------------
			session.getTransaction().commit();
			session.close(); // 游离状态
		}
	//2.2 HQL语句批量查询时,查询结果是否会进入缓存? 查询结果会放入缓存中
		@Test
			public void fun3(){
				Session session = HibernateUtils.openSession();
				session.beginTransaction();
				//------------------------------------------------
				
				List<User> list1 = session.createQuery("from User").list();
				
				User u = (User) session.get(User.class, 1);
				//------------------------------------------------
				session.getTransaction().commit();
				session.close(); // 游离状态
			}
		@Test
		//3.1 SQL查询 结果会不会放入1级缓存中? 如果把查询结果封装到对象中,对象会放入一级缓存
		public void fun4(){
			Session session = HibernateUtils.openSession();
			session.beginTransaction();
			//------------------------------------------------
			
			List<User> list1 = session.createSQLQuery("select * from t_user").addEntity(User.class).list();
			
			User u = (User) session.get(User.class, 1);
			
			System.out.println(u);
			//------------------------------------------------
			session.getTransaction().commit();
			session.close(); // 游离状态
		}	
		@Test
		//3.2 SQL查询 结果会不会放入1级缓存中?没有把查询结果封装到对象中,对象不会放入一级缓存
		public void fun5(){
			Session session = HibernateUtils.openSession();
			session.beginTransaction();
			//------------------------------------------------
			
			List list1 = session.createSQLQuery("select * from t_user").list();
			
			User u = (User) session.get(User.class, 1);
			
			System.out.println(u);
			//------------------------------------------------
			session.getTransaction().commit();
			session.close(); // 游离状态
		}	
		
		//criteria => 会将查询结果放入一级缓存. 但是查询不会使用一级缓存. 与Hql查询结论一致.
}
