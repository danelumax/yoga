package com.thread;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadPoolTest {

	public static void main(String[] args) throws Exception {
		ExecutorService pool = Executors.newFixedThreadPool(6);
		Count target = new Count(0);
		
		pool.submit(target);
		pool.submit(target);
		pool.submit(target);
		
		pool.shutdown();
	}
}
