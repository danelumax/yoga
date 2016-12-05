package com.collection.list;

import java.util.ArrayList;
import java.util.List;

public class TraverseList {
	
	public static void main(String[] args) {
		List<Page> book = new ArrayList<>();
		for(int i=0; i<10; i++) {
			book.add(new Page(i));
		}
		
		/* easy traverse */
		for(Page page : book) {
			System.out.println(page.getIndex());
		}
	}
}
