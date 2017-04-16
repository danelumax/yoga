package com.jcg.examples.test;


import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.core.io.ClassPathResource;

import com.jcg.examples.entity.Person;
import com.jcg.examples.repo.PersonRepo;


public class Application {
	
	public static void ListAllPerson(Iterable<Person> personList) {
		for (Person person : personList) {
			System.out.println(person);
        }
	}
	
	public static void main(String[] args) {
	    ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(new ClassPathResource("spring-config.xml").getPath());
		PersonRepo personRepo = context.getBean(PersonRepo.class);
		
		//add person (1, Achilles)
		Person personAchilles = new Person();
		personAchilles.setpId(1);
		personAchilles.setName("Achilles");
		personRepo.save(personAchilles);
		
		//add person (2, Hektor)
		Person personHektor = new Person();
		personHektor.setpId(2);
		personHektor.setName("Hektor");
		personRepo.save(personHektor);
		
		//add person (3, Liwei)
		Person Liwei = new Person();
		Liwei.setpId(3);
		Liwei.setName("Liwei");
		personRepo.save(Liwei);
		
		//add person (4, Yoga)
		Person Yoga = new Person();
		Yoga.setpId(4);
		Yoga.setName("Yoga");
		personRepo.save(Yoga);
		
		System.out.println("\nPerson List before deleting: ");
		Iterable<Person> personList = personRepo.findAll();
		Application.ListAllPerson(personList);
		
		Person deletePerson = new Person();
		deletePerson.setpId(1);
		personRepo.delete(deletePerson);
		
		System.out.println("\nPerson List after deleting: ");
		personList = personRepo.findAll();
		Application.ListAllPerson(personList);
			
		context.close();
	}
}
