package com.collection.list.linkedlist;

import java.util.LinkedList;

public class LinkedListStack {

	public static void main(String[] args) {
		int size = 0;
		LinkedList<Integer> stack = new LinkedList<>();
		/* input sequence: 0,1,2,3,4,5,6,7,8,9 */
		for(int i=0; i<10; i++) {
			stack.push(i);
			//stack.offerFirst(i);
		}
		
		size = stack.size();
		System.out.println("Stack Size: " + stack.size());
		/* out sequence: 9,8,7,6,5,4,3,2,1,0 */
		for(int i=0; i<size; i++) {
			System.out.println(stack.pop());
			//System.out.println(stack.removeFirst());
		}
	}
}
