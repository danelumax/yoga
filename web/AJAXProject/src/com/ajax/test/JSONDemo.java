package com.ajax.test;

import java.util.ArrayList;
import java.util.List;

import org.junit.Test;

import com.ajax.pojo.Product;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import net.sf.json.JsonConfig;

public class JSONDemo {
	@Test
	public void test1(){
		String s[] = {"a","b","c"};
		JSONArray json = JSONArray.fromObject(s);
		System.out.println(json);
	}
	@Test
	public void test2(){
		List<String> list = new ArrayList<String>();
		list.add("a");
		list.add("b");
		list.add("c");
		JSONArray json = JSONArray.fromObject(list);
		System.out.println(json);
	}
	@Test
	public void test3(){
		List<Product> list = new ArrayList<Product>();
		list.add(new Product(1, "金瓶梅", 20));
		list.add(new Product(2, "葵花", 20));
		JSONArray json = JSONArray.fromObject(list);
		System.out.println(json);
	}
	@Test
	public void test4(){
		Product p = new Product(1, "金瓶梅", 20);
		JSONObject json = JSONObject.fromObject(p);
		System.out.println(json);
	}
	//过滤
	@Test
	public void test5(){
		Product p = new Product(1, "金瓶梅", 20);
		JsonConfig jc = new JsonConfig();
		jc.setExcludes(new String[]{"id"});
		JSONObject json = JSONObject.fromObject(p,jc);
		System.out.println(json);
	}
}
