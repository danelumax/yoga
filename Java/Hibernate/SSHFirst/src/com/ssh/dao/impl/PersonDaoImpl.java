package com.ssh.dao.impl;

import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.ssh.dao.PersonDao;
import com.ssh.pojo.Person;

@Repository
public class PersonDaoImpl implements PersonDao {

	@Autowired
	private SessionFactory sessionFactory;
	
	@Override
	public void save(Person person) {
		sessionFactory.getCurrentSession().save(person);
	}

}
