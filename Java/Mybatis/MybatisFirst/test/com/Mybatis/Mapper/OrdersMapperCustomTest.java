package com.Mybatis.Mapper;

import java.io.InputStream;
import java.util.List;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.Before;
import org.junit.Test;

import com.pojo.Orders;
import com.pojo.OrdersCustom;
import com.pojo.User;

public class OrdersMapperCustomTest {

	private SqlSessionFactory sqlSessionFactory;

	// 此方法是在执行testFindUserById之前执行
	@Before
	public void setUp() throws Exception {
		// 创建sqlSessionFactory

		// mybatis配置文件
		String resource = "SqlMapConfig.xml";
		// 得到配置文件流
		InputStream inputStream = Resources.getResourceAsStream(resource);

		// 创建会话工厂，传入mybatis的配置文件信息
		sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
	}

	@Test
	public void testFindOrdersUser() throws Exception {

		SqlSession sqlSession = sqlSessionFactory.openSession();
		// 创建代理对象
		OrdersMapperCustom ordersMapperCustom = sqlSession.getMapper(OrdersMapperCustom.class);

		// 调用maper的方法
		List<OrdersCustom> list = ordersMapperCustom.findOrdersUser();

		System.out.println(list);

		sqlSession.close();
	}
	

	@Test
	public void testFindOrdersUserResultMap() throws Exception {

		SqlSession sqlSession = sqlSessionFactory.openSession();
		// 创建代理对象
		OrdersMapperCustom ordersMapperCustom = sqlSession
				.getMapper(OrdersMapperCustom.class);

		// 调用maper的方法
		List<Orders> list = ordersMapperCustom.findOrdersUserResultMap();

		System.out.println(list);

		sqlSession.close();
	}
	
	@Test
	public void testCache2() throws Exception {
		SqlSession sqlSession1 = sqlSessionFactory.openSession();
		SqlSession sqlSession2 = sqlSessionFactory.openSession();
		SqlSession sqlSession3 = sqlSessionFactory.openSession();
		
		/* need sql */
		UserMapper userMapper1 = sqlSession1.getMapper(UserMapper.class);
		User user1 = userMapper1.findUserById(1);
		System.out.println(user1);
		
		//这里执行关闭操作，将sqlsession中的数据写到二级缓存区域
		sqlSession1.close();
		
//		/* clean cache */
//		UserMapper userMapper3 = sqlSession3.getMapper(UserMapper.class);
//		User user3 = userMapper3.findUserById(1);
//		user3.setUsername("Liwei");
//		userMapper3.updateUser(user3);
//		//执行提交，清空UserMapper下边的二级缓存
//		sqlSession3.commit();
//		sqlSession3.close();
		
		UserMapper userMapper2 = sqlSession2.getMapper(UserMapper.class);
		User user2 = userMapper2.findUserById(1);
		System.out.println(user2);
		
		sqlSession1.close();
	}

}
