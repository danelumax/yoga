package com.controller;


import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
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
import com.registration.RentDate;

import org.springframework.ui.ModelMap;


@Controller
public class RegisterController {
	private ModelMysqlManager mysqlManager;
	public RegisterController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}
	
	@RequestMapping(value = "/mainPage", method = RequestMethod.GET)
	public ModelAndView mainPage() {
		RentDate date = mysqlManager.getInitialStudent();
		return new ModelAndView("insertPage", "command", date);
	}
	
	@RequestMapping(value = "/insertRentInfo", method = RequestMethod.POST)
	public String addStudent(@ModelAttribute("command")RentDate date, ModelMap model) throws Exception {
		checkAttribute(date);
		
		/* for properties */
		//ModelPropertiesManager.getInstance().saveModeltoProperties(student);
				
		/* for mysql */
		mysqlManager.saveModeltoMysql(date);
		
		mysqlManager.showView(model);
		
		return "result";
	}
	
	@ExceptionHandler({SpringException.class})
	public void checkAttribute(RentDate date) {
		System.out.println(date.getHostName() + " " + date.getEid());
		
		if(date.getHostName().length() < 2 ) {
			throw new SpringException("Given age is larger 200");
		}
		
		if(date.getEid().length() < 2 ){
			throw new SpringException("Given name is too short");
		}
	}
}