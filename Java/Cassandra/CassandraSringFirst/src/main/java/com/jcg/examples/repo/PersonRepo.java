package com.jcg.examples.repo;

import org.springframework.data.repository.CrudRepository;

import com.jcg.examples.entity.Person;

public interface PersonRepo extends CrudRepository<Person, String> {

}
