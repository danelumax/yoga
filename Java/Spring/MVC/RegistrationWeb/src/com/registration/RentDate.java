package com.registration;

import java.io.Serializable;

public class RentDate implements Serializable {
	private Integer id;
	private String hostName;
	private String eid;
	private Integer duration;
	private String startTime;
	private String leaseTime;
	
	public RentDate() {
	}
	
	public Integer getId() {
		return id;
	}
	public void setId(Integer id) {
		this.id = id;
	}
	public String getHostName() {
		return hostName;
	}
	public void setHostName(String hostName) {
		this.hostName = hostName;
	}
	public String getEid() {
		return eid;
	}
	public void setEid(String eid) {
		this.eid = eid;
	}
	public Integer getDuration() {
		return duration;
	}
	public void setDuration(Integer duration) {
		this.duration = duration;
	}
	public String getStartTime() {
		return startTime;
	}
	public void setStartTime(String startTime) {
		this.startTime = startTime;
	}
	public String getLeaseTime() {
		return leaseTime;
	}
	public void setLeaseTime(String leaseTime) {
		this.leaseTime = leaseTime;
	}
}