package read;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

/*
 * 第一题：现有的程序代码模拟产生了16个日志对象，并且需要运行16秒才能打印完这些日志，
 * 请在程序中增加4个线程去调用parseLog()方法来分头打印这16个日志对象，
 * 程序只需要运行4秒即可打印完这些日志对象。原始代码如下：
 */

public class Test {
	
	public static void main(String[] args) {
		/*
		 * 使用阻塞队列的目的：
		 *  1. 生产线程向队列存放数据， 消费线程只需向队列拿数据，生产-消费实现同步
		 *  2. 如果队列满了（生产快了），存放的线程阻塞
		 *  3. 如果队列空了（消费快了），消费的线程阻塞
		 * 	4. 循环队列，不用考虑队列的容量（1也可以）
		 */
		final BlockingQueue<String> queue = new ArrayBlockingQueue<String>(16);
		for(int i=0;i<4;i++) {
			new Thread(new Runnable() {
				@Override
				public void run() {
					while(true) {
						try {
							String log = queue.take();
							parseLog(log);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
					}
				}
				
			}).start();
		}
		
		System.out.println("begin:"+(System.currentTimeMillis()/1000));
		/*模拟处理16行日志，下面的代码产生了16个日志对象，当前代码需要运行16秒才能打印完这些日志。
		修改程序代码，开四个线程让这16个对象在4秒钟打完。
		*/
		for(int i=0;i<16;i++) {  //这行代码不能改动
			final String log = "" + (i+1);//这行代码不能改动
			{
					try {
						queue.put(log);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
			}
		}
	}
	
	//parseLog方法内部的代码不能改动
	public static void parseLog(String log) {
		System.out.println(log+":"+(System.currentTimeMillis()/1000));
		
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}		
	}
	
}
