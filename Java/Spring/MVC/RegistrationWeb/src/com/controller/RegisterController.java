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

import com.pojo.RentData;
import com.registration.ModelMysqlManager;
import com.registration.SpringException;

import org.springframework.ui.ModelMap;


@Controller
public class RegisterController {
	private ModelMysqlManager mysqlManager;
	public RegisterController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}
	
	@RequestMapping(value = "/registerInfo", method = RequestMethod.GET)
	public ModelAndView registerInfo() {
		RentData date = mysqlManager.getInitialData();
		
		ModelAndView modelAndView = new ModelAndView();
		modelAndView.addObject("command", date);
		modelAndView.setViewName("insertPage");
		
		return modelAndView;
	}
	
	@RequestMapping(value = "/insertRentInfo", method = RequestMethod.POST)
	public String insertRentInfo(@ModelAttribute("command")RentData date, ModelMap model) throws Exception {
		checkAttribute(date);
		
		/* for properties */
		//ModelPropertiesManager.getInstance().saveModeltoProperties(student);
				
		/* for mysql */
		mysqlManager.saveModeltoMysql(date);
		
		List<RentData> list = this.mysqlManager.getAllDate();
		model.addAttribute("list", this.mysqlManager.deleteTimeoutStudent(list));	
		
		return "result";
	}
	
	@ExceptionHandler({SpringException.class})
	public void checkAttribute(RentData date) {
		System.out.println(date.getHostName() + " " + date.getEid());
		
		if(date.getHostName().length() < 2 ) {
			throw new SpringException("Given age is larger 200");
		}
		
		if(date.getEid().length() < 2 ){
			throw new SpringException("Given name is too short");
		}
	}
}