package com.search.deepfirstsearch;

/*
 * 方法：
 * 1. 构造一个指定打下的栈
 * 2. 压栈
 * 3. 出栈
 * 4. 查看栈顶数据
 * 5. 判断栈是否为空
 * 5. 判断栈是否为慢
 */

public class MyStack {
	//底层实现是一个数组
	private long[] arr;
	private int top;
	
	/**
	 * 带参数构造方法，参数为数组初始化大小
	 */
	public MyStack(int maxsize) {
		arr = new long[maxsize];
		//为了第一个压入数据的下标是0
		top = -1;
	}
	
	/**
	 * 添加数据
	 */
	public void push(int value) {
		//先移动top，然后添加数据
		arr[++top] = value;
	}
	
	/**
	 * 移除数据
	 */
	public long pop() {
		//先返回数据，然后下移top
		return arr[top--];
	}
	
	/**
	 * 查看数据
	 */
	public long peek() {
		return arr[top];
	}
	
	/**
	 * 判断是否为空
	 */
	public boolean isEmpty() {
		return top == -1;
	}
	
	/**
	 * 判断是否满了
	 */
	public boolean isFull() {
		//不能大于数组的下标极限
		return top == arr.length - 1;
	}
}
