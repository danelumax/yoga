package com.form;


import java.util.List;

import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.ui.ModelMap;

@Controller
public class StudentController {
	@RequestMapping(value = "/student", method = RequestMethod.GET)
	public ModelAndView student() {
		return new ModelAndView("student", "command", new Student());
	}
	
	@RequestMapping(value = "/addStudent", method = RequestMethod.POST)
	public String addStudent(@ModelAttribute("command")Student student, ModelMap model) throws Exception {
//		ModelManager manager = new ModelManager("C://Users//eliwech//Desktop//OS//yoga//Java//Spring//MVC//FormTest//resource//store.properties");
//		manager.initProperties();
//		manager.saveStudent(student);
//		
//		
//		final String dropSQL = "drop table if exists student_table";
//		final String createSQL = "create table student_table ( " +
//				  				 "student_id int auto_increment primary key, " +
//				  				 "student_name varchar(255)," +
//				  				 "student_age int)";
//		//final String insertSQL = "insert into student_table(student_name) values('Liwei')";
//		final String selectSQL = "select * from student_table";
//		
//		ExecuteSQL es = new ExecuteSQL();
//		
////		System.out.println("----- Delete Existed Table -----");
////		es.executeSql(dropSQL);
//		
////		System.out.println("----- Create Table -----");
////		es.executeSql(createSQL);
//		
//		System.out.println("----- Insert Data -----");
//		es.executeSql("insert into student_table(student_name) values('" + student.getName() + "')");
//		
//		System.out.println("----- Query Data -----");
//		es.executeSql(selectSQL);
		
		
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		StudentDAOImpl studentDAOImpl = 
				(StudentDAOImpl)context.getBean("studentDAOImpl");
		
		System.out.println("------Records Creation--------" );
	    studentDAOImpl.create(student.getName(), student.getAge());
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
	    //Student student = studentDAOImpl.getStudent(2);
	    System.out.print("ID : " + student.getId() );
	    System.out.print(", Name : " + student.getName() );
	    System.out.println(", Age : " + student.getAge());  
		
		
		
		model.addAttribute("name", "Liwei: " + student.getName());
		model.addAttribute("age", student.getAge());
		model.addAttribute("id", student.getId());      
		return "result";
	}
}