package com.thread.test;
/*
 线程常用的方法：
 	 Thread(String name)     初始化线程的名字
	 setName(String name)    设置线程对象名
	 getName()             返回线程的名字
	 
	 
	 sleep()                 线程睡眠指定的毫秒数。 静态的方法， 那个线程执行了sleep方法代码那么就是那个线程睡眠。
	 
	 currentThread()      返回当前的线程对象，该方法是一个静态的方法， 注意： 那个线程执行了currentThread()代码就返回那个线程 的对象。
	 
	 getPriority()             返回当前线程对象的优先级   默认线程的优先级是5
	 setPriority(int newPriority) 设置线程的优先级    虽然设置了线程的优先级，但是具体的实现取决于底层的操作系统的实现（最大的优先级是10 ，最小的1 ， 默认是5）。
	 
 */
public class ThreadBasicFunction extends Thread {
	
	public ThreadBasicFunction(String name){
		super(name); //调用了Thread类的一个 参数的构造方法。
	}
	
	
	@Override
	public void run() {
		/*System.out.println("this:"+ this);
		System.out.println("当前线程对象：" + Thread.currentThread());	*/
		
		for (int i = 0; i < 100 ; i++) {
			System.out.println(Thread.currentThread().getName()+":"+i);
			
			
			/*try {
				Thread.sleep(100);  //为什么在这里不能抛出异常，只能捕获？？ Thread类的run方法没有抛出异常类型，所以子类不能抛出异常类型。
			} catch (InterruptedException e) {
				e.printStackTrace();
			} */
		}
		
		
	}
	
	
	public static void main(String[] args) throws InterruptedException {
		//创建了一个线程对象
		ThreadBasicFunction d = new ThreadBasicFunction("狗娃");
		d.setPriority(10); //设置线程 的优先级。 优先级的数字越大，优先级越高  ， 优先级的范围是1~10
		d.start();
		
		for (int i = 0; i < 100 ; i++) {
			System.out.println(Thread.currentThread().getName()+":"+i);
		}
		
		/*
		System.out.println("自定义线程的优先级："+d.getPriority());  //线程的优先级默认是5
		System.out.println("主线程的优先级："+Thread.currentThread().getPriority());
		
		
		d.start();
		
		d.setName("铁蛋"); //setName设置线程的名字
		d.start(); //开启线程 
		
		Thread mainThread = Thread.currentThread();
		System.out.println("主线程的名字："+ mainThread.getName());
	*/
	}

}
