package com.jdbctemplate;

import java.util.List;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {

	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		StudentDAOImpl studentDAOImpl = 
				(StudentDAOImpl)context.getBean("studentDAOImpl");
		
		System.out.println("------Records Creation--------" );
	    studentDAOImpl.create("Zara", 11);
	    studentDAOImpl.create("Nuha", 2);
	    studentDAOImpl.create("Ayan", 15);
	    
	    System.out.println("------Listing Multiple Records--------" );
	    List<Student> students = studentDAOImpl.listStudents();
	    for (Student record : students) {
	       System.out.print("ID : " + record.getId() );
	       System.out.print(", Name : " + record.getName() );
	       System.out.println(", Age : " + record.getAge());
	    }
	    
	    System.out.println("----Updating Record with ID = 2 -----" );
	    studentDAOImpl.update(2, 20);
	    
	    System.out.println("----Listing Record with ID = 2 -----" );
	    Student student = studentDAOImpl.getStudent(2);
	    System.out.print("ID : " + student.getId() );
	    System.out.print(", Name : " + student.getName() );
	    System.out.println(", Age : " + student.getAge());  
	}

}
