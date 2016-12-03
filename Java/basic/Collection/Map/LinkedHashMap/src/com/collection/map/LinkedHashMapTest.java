package com.collection.map;

import java.util.LinkedHashMap;

public class LinkedHashMapTest {

	public static void main(String[] args) {
		LinkedHashMap<String, Integer> scores = new LinkedHashMap<>();
		scores.put("Chinese", 80);
		scores.put("English", 82);
		scores.put("Math", 76);
		
		/* use keySet to traverse, so easy ! */ 
		for (String key : scores.keySet()) {
			System.out.println(key + "-->" + scores.get(key));
		}
	}
}
