package com.controller;


import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import com.registration.ModelMysqlManager;
import com.registration.SpringException;
import com.registration.Student;

import org.springframework.ui.ModelMap;


@Controller
public class StudentController {
	private ModelMysqlManager mysqlManager;
	public StudentController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}
	
	@RequestMapping(value = "/student", method = RequestMethod.GET)
	public ModelAndView mainPage() {
		Student student = mysqlManager.getInitialStudent();
		return new ModelAndView("insertPage", "command", student);
	}
	
	@RequestMapping(value = "/addStudent", method = RequestMethod.POST)
	public String addStudent(@ModelAttribute("command")Student student, ModelMap model) throws Exception {
		checkAttribute(student);
		
		/* for properties */
		//ModelPropertiesManager.getInstance().saveModeltoProperties(student);
		
		/* for mysql */
		mysqlManager.saveModeltoMysql(student);
		
		mysqlManager.showView(model);
		
		return "result";
	}
	
	@ExceptionHandler({SpringException.class})
	public void checkAttribute(Student student) {
		if(student.getAge() > 200) {
			throw new SpringException("Given age is larger 200");
		}
		
		if(student.getName().length() < 2 ){
			throw new SpringException("Given name is too short");
		}
		
		if(student.getId() < 0 ){
			throw new SpringException("Given id is smaller than 0");
		}
	}
}