package com.registration;

import java.sql.Timestamp;
import java.util.Date;


public class TimeUtils {
	static public long getLeaseTime(String registerTime) {
		Date currentTime = new Date();
		Timestamp registerTimeStamp =Timestamp.valueOf(registerTime);
		long leaseTime = currentTime.getTime() - registerTimeStamp.getTime();
		
		return leaseTime / 1000;
	}
	
	static public String getFormatLeaseTime(String registerTime) {
		long leaseTimeSecond = getLeaseTime(registerTime);
		
		int day = (int)(leaseTimeSecond / (24 * 3600));
		int hour = (int)(leaseTimeSecond / 3600 - day * 24);
		int minute = (int)(leaseTimeSecond % 3600 / 60);
		int second = (int)(leaseTimeSecond % 60);
		String formatTime = day + " days, " + hour + " hours, " + minute + " minutes, " + second + " seconds";
		
		return formatTime;
	}
	
	static boolean isTimeout(String registerTime, int duration) {
		boolean ret = false;
		long leaseTimeSecond = getLeaseTime(registerTime);
		if (leaseTimeSecond > duration * 60) {
			ret = true;
		}
		
		return ret;
	}
}
