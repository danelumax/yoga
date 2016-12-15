package com.controller;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.registration.ModelMysqlManager;
import com.registration.Student;

@Controller
public class HomeController {
	private ModelMysqlManager mysqlManager;
	public HomeController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(ModelMap model){
		mysqlManager.showView(model);
		return "home";
	}
}
