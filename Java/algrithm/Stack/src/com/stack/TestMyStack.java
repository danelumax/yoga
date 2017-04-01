package com.stack;

public class TestMyStack {
	public static void main(String[] args) {
		//1. 创建一个指定长度的栈
		MyStack ms = new MyStack(4);
		//2. 依次压入数据
		ms.push(23);
		ms.push(12);
		ms.push(1);
		ms.push(90);
		System.out.println(ms.isEmpty());
		System.out.println(ms.isFull());
		
		//3. 显示栈定数据（最后一个压入的）
		System.out.println(ms.peek());
		
		//4. 依次弹出数据
		while(!ms.isEmpty()) {
			System.out.print(ms.pop() + " ");
		}
		System.out.println();
		
		//5. 判断栈情况
		System.out.println(ms.isEmpty());
		System.out.println(ms.isFull());
	}
}
