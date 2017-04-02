package com.queue;
/*
 * 循环列队
 * 方法：
 * 1. 创建指定大小的循环队列
 * 2. 从队尾插入数据
 * 3. 从队首删除数据
 * 4. 查看队首元素
 * 5. 判断队列是否为空
 * 6. 判断队列是否为满
 */
public class MyCycleQueue {
	//底层使用数组
	private long[] items;
	//有效数据的大小
	private int count;
	//队头
	private int front;
	//队尾
	private int end;
	
	/**
	 * 带参数的构造方法，参数为数组的大小
	 */
	public MyCycleQueue(int maxsize) {
		items = new long[maxsize];
	}
	
	/**
	 * 添加数据,从队尾插入
	 */
	public void enqueue(long value) {
		//先添加数据，然后再移动end位置
		items[end] = value;
		if (++end == items.length) {
			end = 0;
		}
		count++;
	}
	
	/**
	 * 删除数据，从队首删除
	 */
	public long dequeue() {
		long value = items[front];
		//只要后移front位置就可以了
		if (++front == items.length) {
			front = 0;
		}
		count--;
		return value;
	}
	
	/**
	 * 查看数据，从队头查看
	 */
	public long peek() {
		return items[front];
	}
	
	/**
	 * 判断是否为空
	 */
	public boolean isEmpty() {
		return count == 0;
	}
	
	/**
	 * 判断是否满了
	 */
	public boolean isFull() {
		return count == items.length;
	}
}
