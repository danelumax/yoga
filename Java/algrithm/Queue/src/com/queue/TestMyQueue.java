package com.queue;

public class TestMyQueue {
	
	public static void main(String[] args) {
		//1. 构建循环队列
		MyCycleQueue mq = new MyCycleQueue(4);
		//2. 添加数据
		mq.enqueue(23);
		mq.enqueue(45);
		mq.enqueue(13);
		mq.enqueue(1);
		System.out.println(mq.isFull());
		System.out.println(mq.isEmpty());
		
		//3. 显示队首元素（第一个插入的）
		System.out.println(mq.peek());
		
		//4. 依次删除队列所有元素
		while (!mq.isEmpty()) {
			System.out.print(mq.dequeue() + " ");
		}
		System.out.println();
		
		//5. 再次添加数据
		mq.enqueue(50);
		mq.enqueue(60);
		mq.enqueue(70);
		mq.enqueue(80);
		
		//6. 再次依次删除队列所有元素
		while (!mq.isEmpty()) {
			System.out.print(mq.dequeue() + " ");
		}
	}
}
