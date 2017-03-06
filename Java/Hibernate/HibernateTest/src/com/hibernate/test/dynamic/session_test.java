package com.hibernate.test.dynamic;

import org.hibernate.Transaction;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
import com.hibernate.test.utils.HibernateUtils;

//dynamic-insert:动态插入 默认值是false
//		true=>如果字段值为null,不参与insert语句
//dynamic-update:动态更新  默认值"false"
//		true=> 没改动过的属性,将不会生成到update语句中
public class session_test {
	@Test
	//演示dynamic-insert 
	public void fun1(){
		org.hibernate.Session session = HibernateUtils.openSession();
		Transaction ts = session.beginTransaction();
		
		User u = new User();
		u.setName("zhangsan");
		//如果属性password的dynamic-insert为true， insert语句中只有name
		//调用Session的save方法保存对象到数据库中
		session.save(u);
		
		ts.commit();
		//关闭资源
		session.close();
	}
	@Test
	//演示dynamic-update
	public void fun2(){
		org.hibernate.Session session = HibernateUtils.openSession();
		
		Transaction ts = session.beginTransaction();
		
		User u = (User) session.get(User.class, 1);
		
		u.setName("jerry");
		
		//如果属性password的dynamic-update为true， 如果password没有修改，update语句中只有name
		session.update(u);
		
		ts.commit();
		//关闭资源
		session.close();
	}
}
