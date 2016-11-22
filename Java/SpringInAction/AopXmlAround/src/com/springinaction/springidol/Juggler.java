package com.springinaction.springidol;

public class Juggler implements Performer {
	
	private int ballNum;
	
	public void setBallNum(int ballNum) {
		this.ballNum = ballNum;
	}
	public int getBallNum(int ballNum) {
		return this.ballNum;
	}
	
	@Override
	public void perform() {
		System.out.println("# Juggler " + this.ballNum + " Bean Bags ... #");
			
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
}