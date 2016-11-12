package com.collection;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {

	public static void main(String[] args) 
		throws IOException {
		List<BeanParent> addressList;
		Set<String> addressSet;
		Map<Integer, String> addressMap;
		Properties addressProp;
		ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
		JavaCollection obj = (JavaCollection)context.getBean("javaCollection");
		
		addressList = obj.getAddressList();
		System.out.println("List Element :");
		for(BeanParent bean : addressList) {
			bean.say();
		}
		
		addressSet = obj.getAddressSet();
		System.out.println("Set Element : " + addressSet);
		
		addressMap = obj.getAddressMap();
		System.out.println("Map Element : " + addressMap);
		
		addressProp = obj.getAddressProp();
		System.out.println("Properties Element : " + addressProp);
	}

}
