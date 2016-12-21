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
	private RentData rentData;

	public RentData getRentData() {
		return rentData;
	}

	public void setRentData(RentData rentData) {
		this.rentData = rentData;
	}

	public MysqlDAO getMysqlDAO() {
		return mysqlDAO;
	}

	public void setMysqlDAO(MysqlDAO mysqlDAO) {
		this.mysqlDAO = mysqlDAO;
	}
	
	public RentData getInitialData() {
		return this.rentData;
	}

	public void saveModeltoMysql(RentData date) {
	    System.out.println("---- Save Web input into Mysql Database -----" );
	    
		Date currentTime = new Date();
		String currentTimeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(currentTime);
		date.setStartTime(currentTimeFormat);
	    
	    this.mysqlDAO.insert(date.getHostName(), date.getEid(), date.getDuration(), date.getStartTime());
	}
	
	public List<RentData> getAllDate() {
		return this.mysqlDAO.listAllDate();
	}
	
	public List<RentData> deleteTimeoutStudent(List<RentData> list) {
		Iterator<RentData> it = list.iterator();
		while(it.hasNext()) {
			RentData tmpDate = (RentData)it.next();
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
