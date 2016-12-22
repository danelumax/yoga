package com.controller;

import java.util.List;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.pojo.RentData;
import com.registration.ModelMysqlManager;

@Controller
public class HomeController {
	private ModelMysqlManager mysqlManager;
	
	public HomeController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}

	@RequestMapping(value = "/home", method = RequestMethod.GET)
	public String home(ModelMap model){
		List<RentData> list = this.mysqlManager.getAllDate();
		model.addAttribute("list", this.mysqlManager.deleteTimeoutStudent(list));
		return "home";
	}
}
