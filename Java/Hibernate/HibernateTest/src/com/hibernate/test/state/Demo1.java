package com.hibernate.test.state;

import org.hibernate.Session;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
import com.hibernate.test.utils.HibernateUtils;
//对象的三种状态

// 持久: 有关联,有id
// 瞬时: 无关联,无id
// 游离: 没有关联,有id(与数据库中对应的id)
public class Demo1 {
	@Test
	//演示三种状态
	public void fun1(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		User u = new User();	// 瞬时状态
		u.setName("tom");		// 瞬时状态
		u.setPassword("1234");	// 瞬时状态
		
		session.save(u);		// 持久状态
									//问题: 调用完save方法,数据库中有没有对应记录?
									// 没有对应记录, 但是最终会被同步到数据库中.仍然是持久状态.
		//------------------------------------------------
		session.getTransaction().commit(); // 持久状态
		session.close(); // 游离状态
	}
	
	// 瞬时 => 持久
	@Test
	public void fun2(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		User u = new User();	// 瞬时状态
		u.setName("tom");		// 瞬时状态
		u.setPassword("1234");	// 瞬时状态
		
		session.save(u);		// 持久状态   save方法会使用主键生成策略,为User指定id. => 
																	//主键自增 => 打印 insert语句
		//------------------------------------------------			// increment=> select max(id) ....
																	//assigned => 需要手动指定主键,不指定将会报错
		session.getTransaction().commit(); // 持久状态
									//事务提交时,会把持久化状态对象同步到数据库中
		session.close(); // 游离状态
	}
	
	// 瞬时=> 游离
	// 瞬时: 没有关联,没有id
	// 游离: 没有关联,有id(与数据库中对应的id)
	@Test
	public void fun3(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		User u = new User();	// 瞬时状态
		
		u.setId(1);	//游离  , 之前没有关联
		
		//----------------------------------------------------
		session.getTransaction().commit(); 
									
		session.close(); 
	}
	
	// 持久=> 瞬时     持久=> 游离=> 瞬时
	// 持久: 有关联,有id
	// 瞬时: 无关联,无id
	@Test
	public void fun4(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 1); // 持久状态
		
		//----------------------------------------------------
		session.getTransaction().commit(); // 持久状态
									//事务提交时,会把持久化状态对象同步到数据库中
		session.close(); // 游离状态
		u.setId(null);//瞬时状态
	}
	
	// 持久=> 瞬时
	// 持久: 有关联,有id
	// 瞬时: 无关联,无id
	@Test
	public void fun5(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 1); // 持久状态
		
		session.evict(u);//将User对象与session的关联移除
		
		u.setId(null);//瞬时状态， , 之前没有关联
		
		session.save(u);//持久状态
		//----------------------------------------------------
		session.getTransaction().commit(); // 持久状态
									//事务提交时,会把持久化状态对象同步到数据库中
		session.close(); // 游离状态
	}

	// 持久=> 游离
	// 只需要将session的关联取消
	@Test
	public void fun6(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 1); // 持久状态
		
		session.evict(u);//游离
		//----------------------------------------------------
		session.getTransaction().commit(); // 游离状态
		session.close(); // 游离状态
	}
		
	// 游离=> 瞬时
	// 移除ID 
	@Test
	public void fun7(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
			//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 1); // 持久状态
		
		session.evict(u);//游离
		
		u.setId(null);// 瞬时
		//----------------------------------------------------
		session.getTransaction().commit(); // 瞬时状态
		session.close(); // 瞬时状态
	}
	
	// 游离=> 持久
	// 是否与Session关联
	@Test
	public void fun8(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 1); // 持久状态
		
		session.evict(u);//游离
		
		session.update(u);//持久
		//----------------------------------------------------
		session.getTransaction().commit(); // 持久状态 -> 打印update语句
		session.close(); // 瞬时状态
	}
	
	/* 三种状态有什么用? */
	// 持久状态,我们使用Hibernate主要是为了持久化我们的数据.
	// 对于对象的状态,我们期望我们需要同步到数据库的数据,都被装换成持久状态
	
	/* 持久化状态特点: Hibernate会自动将持久化状态对象的变化同步到数据库中 */
	@Test
	public void fun9(){
		Session session = HibernateUtils.openSession();
		session.beginTransaction();
		//------------------------------------------------
		//通过get方法,得到持久状态对象
		User u= (User) session.get(User.class, 6); // 持久状态
	
		u.setName("jerry");//持久状态
	
		//u.setId(3);//与session建立关联的对象的ID,不允许修改.
	
		//session.update(u);// 多余=> 因为Hibernate会自动将持久化状态对象的变化同步到数据库中.
		//----------------------------------------------------
		session.getTransaction().commit(); // 持久状态 -> 打印update语句
		session.close(); 
	}
	
}
