package com.zhenti.observerPattern;

public class Main {

	public static void main(String[] args) {
		Reader reader1 = new Reader("Reader1");
		Reader reader2 = new Reader("Reader2");
		Newspaper newspaper = new Newspaper();
		//观察者注册
		newspaper.registerObserver(reader1);
		newspaper.registerObserver(reader2);
		//触发
		newspaper.setMsg("message");
	}

}
