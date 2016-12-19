package com.registration;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import org.springframework.ui.ModelMap;

public class ModelMysqlManager {
	private MysqlDAO mysqlDAO;
	private RentDate rentDate;

	public RentDate getRentDate() {
		return rentDate;
	}

	public void setRentDate(RentDate rentDate) {
		this.rentDate = rentDate;
	}

	public MysqlDAO getMysqlDAO() {
		return mysqlDAO;
	}

	public void setMysqlDAO(MysqlDAO mysqlDAO) {
		this.mysqlDAO = mysqlDAO;
	}
	
	public RentDate getInitialStudent() {
		return this.rentDate;
	}

	public void saveModeltoMysql(RentDate date) {
	    System.out.println("---- Save Web input into Mysql Database -----" );
	    
		Date currentTime = new Date();
		String currentTimeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(currentTime);
		date.setStartTime(currentTimeFormat);
	    
	    this.mysqlDAO.insert(date.getHostName(), date.getEid(), date.getDuration(), date.getStartTime());
	}
	
	public void showView(ModelMap model) {
		System.out.println("---- Query Student from Mysql Database -----" );
		List<RentDate> list = this.mysqlDAO.listAllDate();
		model.addAttribute("list", deleteTimeoutStudent(list)); 
	}
	
	public List<RentDate> getAllDate() {
		return this.mysqlDAO.listAllDate();
	}
	
	public List<RentDate> deleteTimeoutStudent(List<RentDate> list) {
		Iterator<RentDate> it = list.iterator();
		while(it.hasNext()) {
			RentDate tmpDate = (RentDate)it.next();
			if(TimeUtils.isTimeout(tmpDate.getStartTime(), tmpDate.getDuration())) {
				System.out.println(tmpDate.getHostName() + " is timeout!");
				this.mysqlDAO.delete(tmpDate.getId());
				it.remove();
				tmpDate = null;
			} else {
				String leaseTime = TimeUtils.getFormatLeaseTime(tmpDate.getStartTime());
				tmpDate.setLeaseTime(leaseTime);
			}
		}
		
		return list;
	}
}
