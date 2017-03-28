package com.spring.autowired.dao.impl;

import org.springframework.stereotype.Component;

import com.spring.autowired.dao.PersonDao;

/*
 * 如果是Autowired使用，就不需要定义bean id了
 */
@Component
public class PersonDaoImpl implements PersonDao {

	@Override
	public void savePerson() {
		System.out.println("PersonDaoImpl::savePerson");
		int a = 1/0;

	}

	@Override
	public void updatePerson() {
		System.out.println("PersonDaoImpl::updatePerson");
		Long.parseLong("aaa");
	}

}
