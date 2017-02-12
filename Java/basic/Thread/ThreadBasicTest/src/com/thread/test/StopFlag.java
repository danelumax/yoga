package com.thread.test;
/*
 线程的停止：
 	1. 停止一个线程 我们一般都会通过一个变量去控制的。
 	2. 如果需要停止一个处于等待状态下的线程，那么我们需要通过变量配合notify方法或者interrupt()来使用。
 */


public class StopFlag extends Thread {
	
	boolean flag = true;
	
	public StopFlag(String name){
		super(name);
	}
	
	
	@Override
	public synchronized void run() {
		int i = 0 ;
		while(flag){
/*			try {
				this.wait(); //狗娃等待..
			
			} catch (InterruptedException e) {
				System.out.println("接收到了异常了....");
			}*/
			System.out.println(Thread.currentThread().getName()+":"+i);
			i++;
		}
	}
	
	
	
	public static void main(String[] args) {
		StopFlag d = new StopFlag("狗娃");
		d.setPriority(10);
		d.start();
		
		for(int i = 0 ; i<100 ; i++){
			System.out.println(Thread.currentThread().getName()+":"+i);
			//当主线程的i是80的时候停止狗娃线程。
			//d.interrupt();  // interrupt()根本就是无法停止一个线程。
			if(i==80){
				d.flag = false;
				//d.interrupt(); //把线程的等待状态强制清除，被清除状态的线程会接收到一个InterruptedException。 
				/*synchronized (d) {					
					d.notify();
				}*/
				
				
			}
			
		}
		
		
	}

}
