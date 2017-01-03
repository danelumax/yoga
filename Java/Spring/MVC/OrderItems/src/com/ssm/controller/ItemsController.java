package com.ssm.controller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.ssm.po.ItemsCustom;
import com.ssm.service.ItemsService;


@Controller
//为了对url进行分类管理 ，可以在这里定义根路径，最终访问url是根路径+子路径
//比如：商品列表：/items/queryItems.action
@RequestMapping("/items")
public class ItemsController {
	
	@Autowired
	private ItemsService itemsService;
	
	@RequestMapping("/queryItems")
	public ModelAndView queryItems(HttpServletRequest request)throws Exception{
				
		//测试forward后request是否可以共享
		System.out.println("========== Fetch forward paramenter: " + request.getParameter("id") + " ==========");
		
		// 调用service查找 数据库，查询商品列表
		List<ItemsCustom> itemsList = itemsService.findItemsList(null);
		
		// 返回ModelAndView
		ModelAndView modelAndView = new ModelAndView();
		// 相当 于request的setAttribut，在jsp页面中通过itemsList取数据
		modelAndView.addObject("itemsList", itemsList);

		// 指定视图
		// 下边的路径，如果在视图解析器中配置jsp路径的前缀和jsp路径的后缀，修改为
		// modelAndView.setViewName("/WEB-INF/jsp/items/itemsList.jsp");
		// 上边的路径配置可以不在程序中指定jsp路径的前缀和jsp路径的后缀
		modelAndView.setViewName("items/itemsList");

		return modelAndView;
		
	}
		
	@RequestMapping(value="/editItems",method={RequestMethod.POST,RequestMethod.GET})
	//@RequestParam里边指定request传入参数名称和形参进行绑定。 把itemsCustom中的id属性，与形参items_id 映射
	//通过required属性指定参数是否必须要传入
	//通过defaultValue可以设置默认值，如果id参数没有传入，将默认值和形参绑定。
	public String editItems(Model model,@RequestParam(value="id",required=true) Integer items_id)throws Exception {
		
		//调用service根据商品id查询商品信息
		ItemsCustom itemsCustom = itemsService.findItemsById(items_id);
		
		//通过形参中的model将model数据传到页面
		//相当于modelAndView.addObject方法
		model.addAttribute("itemsCustom", itemsCustom);
		
		return "items/editItems";
	}
		
	//商品信息修改提交
	@RequestMapping("/editItemsSubmit")
	/*
	 * 1. request是上一个页面action过来的消息
	 * 2. request来到controller，
	 *    1> 在request中有一个input name=“id”的，然后遍历controller形参列表，
	 * 	  2> 发现有一个名为id的参数，就把request的id值赋给 形参中的id
	 *    3> 发现有个pojo，并且pojo中的属性名也为id， 就把request的id值赋给 形参中的pojo的id属性。
	 *    4> 如果request另外一个input name与pojo中的属性名一致，那么为pojo赋值第二个属性。
	 *    5> 全部结束后，request中的所有与pojo属性相关的数据，都赋值到pojo中了。 
	 */
	public String editItemsSubmit(HttpServletRequest request,Integer id,ItemsCustom itemsCustom)throws Exception {
		
		//调用service更新商品信息，页面需要将商品信息传到此方法
		itemsService.updateItems(id, itemsCustom);
		
		//重定向到商品查询列表
		//return "redirect:queryItems.action";
		//页面转发
		//return "forward:queryItems.action";
		return "success";
	}

}
