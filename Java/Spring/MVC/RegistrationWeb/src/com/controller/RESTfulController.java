package com.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.registration.ModelMysqlManager;
import com.registration.RentDate;

@RestController
public class RESTfulController {
	private ModelMysqlManager mysqlManager;
	public RESTfulController() {
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		this.mysqlManager = (ModelMysqlManager) context.getBean("modelMysqlManager");
	}
		
	@RequestMapping(value="/rentInfoJSON", method=RequestMethod.GET, headers="Accept=application/json")
	public List<RentDate> getRentInfoJSON() {
		return mysqlManager.getAllDate();
	}
}
