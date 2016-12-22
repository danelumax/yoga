package com.registration;

import java.util.List;
import javax.sql.DataSource;

import com.pojo.RentData;

/* DAO Support Interface */
public interface DAO {
	
	public void setDataSource(DataSource ds);
	
	public void insert(String hostname, String eid, Integer duration, String startTime);
	
	public RentData getStudent(Integer id);
	
	public List<RentData> listAllDate();
	
	public void delete(Integer id);
	
	public void update(String hostname, String eid, Integer duration, String startTime, Integer id);
}	
