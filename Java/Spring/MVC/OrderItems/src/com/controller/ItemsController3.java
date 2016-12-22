package com.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.pojo.Items;


@Controller
public class ItemsController3 {
	
	@RequestMapping("/queryItems")
	public ModelAndView queryItems()throws Exception{
		
		List<Items> itemsList = new ArrayList<Items>();
		
		Items items_1 = new Items();
		items_1.setName("ThinkPad");
		items_1.setPrice(6000f);
		items_1.setDetail("ThinkPad T430");
		
		Items items_2 = new Items();
		items_2.setName("Apple Phone");
		items_2.setPrice(5000f);
		items_2.setDetail("iphone6");
		
		itemsList.add(items_1);
		itemsList.add(items_2);
		
		ModelAndView modelAndView =  new ModelAndView();

		modelAndView.addObject("itemsList", itemsList);
		
		modelAndView.setViewName("itemsList");
		
		return modelAndView;
		
	}

}
