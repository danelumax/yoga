package com.springinaction.springidol;

import org.aspectj.lang.ProceedingJoinPoint;

public class Audience {
	private boolean isSuccessful = false;
	
	public void watchPerformance(ProceedingJoinPoint joinPoint) {
		try {
			System.out.println("The audience is taking their seats ...");
			System.out.println("The audience is turning off their cellphones ...");
			long start = System.currentTimeMillis();
			
			joinPoint.proceed();
			
			long end = System.currentTimeMillis();
			System.out.println("CLAP CLAP CLAP CLAP CLAP ...");
			System.out.println("The performance took " + (end - start) + " milliseconds ...");
			
			if (!isSuccessful) {
				Thread.sleep(500);
				throw new Exception();
			}
		} catch (Throwable t) {
			System.out.println("Boo !!! We want our money back ...");
			t.printStackTrace();
		}
	}
}
