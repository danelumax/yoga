package com.form;

import java.io.FileNotFoundException;
import java.io.IOException;
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
		//saveModeltoProperties(Student);
		
		saveModeltoMysql(student);
		
		showView(student, model);
		return "result";
	}
	
	public void saveModeltoProperties(Student student) throws FileNotFoundException, IOException {
		ModelManager manager = new ModelManager("C://Users//eliwech//Desktop//OS//yoga//Java//Spring//MVC//FormTest//resource//store.properties");
		manager.initProperties();
		manager.saveStudent(student);
	}
	
	public void saveModeltoMysql(Student student) {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		StudentDAOImpl studentDAOImpl = 
				(StudentDAOImpl)context.getBean("studentDAOImpl");
		
		System.out.println("------Records Creation--------" );
	    studentDAOImpl.create(student.getName(), student.getAge());
	    studentDAOImpl.create("Nuha", 2);
	    studentDAOImpl.create("Ayan", 18);
	    
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
	    System.out.print("ID : " + student.getId() );
	    System.out.print(", Name : " + student.getName() );
	    System.out.println(", Age : " + student.getAge());  
	}
	
	public void showView(Student student, ModelMap model) {
		model.addAttribute("name", "Liwei: " + student.getName());
		model.addAttribute("age", student.getAge());
		model.addAttribute("id", student.getId());  
	}
}