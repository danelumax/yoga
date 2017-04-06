package com.zhenti.observerPattern;

import java.util.ArrayList;

public class Newspaper implements Subject {

	//维护observer列表
	private ArrayList<Observer> readers = new ArrayList<>();
	
	private String msg;
	
	@Override
	public void registerObserver(Observer observer) {
		readers.add(observer);
	}

	@Override
	public void removeObserver(Observer observer) {
		readers.remove(observer);
	}

	//遍历通知observer
	@Override
	public void notifyObservers() {
		for(Observer observer : readers) {
			observer.update(msg);
		}
	}
	
	//一旦外部对subject进行修改，马上通知observer
	public void setMsg(String msg) {
		this.msg = msg;
		notifyObservers();
	}

}
