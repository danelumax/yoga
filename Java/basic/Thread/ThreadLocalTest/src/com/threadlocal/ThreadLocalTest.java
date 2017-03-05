package com.threadlocal;

class Message {
	private String title;

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}
}

class Demo {
	private Message msg = MyTran.get();
	public void fun() {
		System.out.println(msg.getTitle());
	}
}

//每一次只能设置一个，而且ThreadLocal会保留当前对象
class MyTran {
	private static ThreadLocal<Message> threadLocal = new ThreadLocal<Message>() ;
	public static void set(Message msg) {
		threadLocal.set(msg);
	}
	public static Message get() {
		return threadLocal.get();
	}
}

//为了保证多个线程可以在自己操作的时候有一个自己的空间，所以应该在保存有当前的线程对象，这样的类凑成的ThreadLocal
//保存： 不同线程在使用相同类时，会生成不同的对象，在ThreadLocal保存时，不同线程会把自己的线程信息与对象一起存在ThreadLocal中，相当于两个不同的key-value对
//获取： 不同线程可以根据自己的线程信息，获取到使用相同类的不同的对象
public class ThreadLocalTest {
	public static void main(String[] args) {
		Thread Thread1 = new Thread(new Runnable() {
			@Override
			public void run() {
				Message msg = new Message();
				msg.setTitle("Thread1 : haha");
				MyTran.set(msg);
				new Demo().fun();
			}
		});
		Thread1.start();
		
		Message msg = new Message();
		msg.setTitle("Thread2 : xixi");
		MyTran.set(msg);
		new Demo().fun();
	}
}

