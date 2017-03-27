package com.spring.aop.exception.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.spring.aop.exception.dao.PersonDao;
import com.spring.aop.exception.service.PersonService;

/*
 * 如果要在xml或context代码中使用bean id，那么@Component必须标明bean id，而且大小写要一致
 */
@Component("personService")
public class PersonServiceImpl implements PersonService {

	//类型匹配，直接用
	@Autowired
	private PersonDao personDao;
	
	public PersonDao getPersonDao() {
		return personDao;
	}

	public void setPersonDao(PersonDao personDao) {
		this.personDao = personDao;
	}

	@Override
	public void savePerson() {
		this.personDao.savePerson();
	}

	@Override
	public void updatePerson() {
		this.personDao.updatePerson();
	}

}
