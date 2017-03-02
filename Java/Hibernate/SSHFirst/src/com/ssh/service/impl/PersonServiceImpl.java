package com.ssh.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ssh.dao.PersonDao;
import com.ssh.pojo.Person;
import com.ssh.service.PersonService;
@Service
public class PersonServiceImpl implements PersonService {

	@Autowired
	private PersonDao personDao;
	
	@Override
	public void save(Person person) {
		personDao.save(person);
	}

}
