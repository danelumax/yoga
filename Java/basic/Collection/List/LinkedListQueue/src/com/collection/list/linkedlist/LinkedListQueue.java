package com.collection.list.linkedlist;

import java.util.LinkedList;

public class LinkedListQueue {

	public static void main(String[] args) {
		int size = 0;
		LinkedList<Integer> stack = new LinkedList<>();
		/* input sequence: 0,1,2,3,4,5,6,7,8,9 */
		for(int i=0; i<10; i++) {
			stack.offer(i); 
			//stack.offerLast(i);
		}
		
		size = stack.size();
		System.out.println("Stack Size: " + stack.size());
		/* out sequence: 0,1,2,3,4,5,6,7,8,9 */
		for(int i=0; i<size; i++) {
			System.out.println(stack.poll());
			//System.out.println(stack.removeFirst());
		}
	}

}
