package com.ssm.mapper;

import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.ssm.po.Items;
import com.ssm.po.ItemsExample;

public class ItemsMapperTest {

	private ApplicationContext applicationContext;
	
	private ItemsMapper itemsMapper;

	@Before
	public void setUp() throws Exception {
		applicationContext = new ClassPathXmlApplicationContext("classpath:spring/applicationContext.xml");
		itemsMapper = (ItemsMapper) applicationContext.getBean("itemsMapper");
	}

	@Test
	public void testSelectByExample() {
		ItemsExample itemsExample = new ItemsExample();
		ItemsExample.Criteria criteria = itemsExample.createCriteria();
		criteria.andNameEqualTo("labtop");
		List<Items> list = itemsMapper.selectByExample(itemsExample);
		
		System.out.println(list);
	}

}
