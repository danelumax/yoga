package com.nio;

import java.nio.CharBuffer;

public class BufferTest {

	public static void main(String[] args) {
		CharBuffer buff = CharBuffer.allocate(8);
		System.out.println("Initial: capacity: " + buff.capacity() + 
						   ", limit: " + buff.limit() +
						   ", position: " + buff.position());
		
		buff.put('a');
		buff.put('b');
		buff.put('c');
		System.out.println("After adding 3 elements, position = " + buff.position());
		
		buff.flip();
		System.out.println("After flip, limit = " + buff.limit() + 
						   ", position = " + buff.position());
		
		System.out.println("The first element(position=0): " + buff.get());
		System.out.println("After get one element, position = " + buff.position());
		
		buff.clear();
		System.out.println("After clear, limit = " + buff.limit() + 
				   		   ", position = " + buff.position());
		
		System.out.println("The Third element: " + buff.get(2));
		System.out.println("After absolutely get, position = " + buff.position());
	}
}
