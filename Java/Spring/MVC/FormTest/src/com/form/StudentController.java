package com.form;


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
	private ApplicationContext context;
	public StudentController() {
		this.context = new ClassPathXmlApplicationContext("Beans.xml");
	}
	
	@RequestMapping(value = "/student", method = RequestMethod.GET)
	public ModelAndView student() {
		return new ModelAndView("insertPage", "command", new Student());
	}
	
	@RequestMapping(value = "/addStudent", method = RequestMethod.POST)
	public String addStudent(@ModelAttribute("command")Student student, ModelMap model) throws Exception {
		ModelMysqlManager mysqlManage = (ModelMysqlManager)this.context.getBean("modelMysqlManager");
		
		/* for properties */
		//ModelPropertiesManager.getInstance().saveModeltoProperties(student);
		
		/* for mysql */
		mysqlManage.saveModeltoMysql(student);
		
		mysqlManage.showView(model);
		
		return "result";
	}
}