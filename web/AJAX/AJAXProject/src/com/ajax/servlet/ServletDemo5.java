package com.ajax.servlet;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.ajax.pojo.Product;

import net.sf.json.JSONArray;

//服务器端返回JSON格式的数据
public class ServletDemo5 extends HttpServlet {
	private List<Product> products = new ArrayList<Product>();
	public void init() throws ServletException {
		products.add(new Product(1, "充气筒", 20));
		products.add(new Product(2, "金瓶梅", 10));
		products.add(new Product(3, "袜子", 10));
		products.add(new Product(4, "洗衣粉", 10));
		products.add(new Product(5, "肥皂", 7));
	}
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.setContentType("text/plain;charset=UTF-8");
		//不是手工组织JSON数据
//		response.getWriter().write("[{id:1,name:'充气筒',price:20},]");
		JSONArray json = JSONArray.fromObject(products);
		response.getWriter().write(json.toString());
		
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}

}
