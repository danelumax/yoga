package com.spring.autowired.test;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.spring.autowired.service.PersonService;


/*	功能：
 * 		用spring的aop做一个统一的异常处理
 *  说明：
 * 		切面的通知是处理异常，而这个异常处理是完全独立于系统之外的内容
 */

public class ExceptionTest {

	@Test
	public void testException() {
		ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
		PersonService personService = (PersonService) context.getBean("personService");
		personService.savePerson();
		//personService.updatePerson();
	}
}
