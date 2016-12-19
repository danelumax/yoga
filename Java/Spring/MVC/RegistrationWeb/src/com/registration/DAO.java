package com.registration;

import java.util.List;
import javax.sql.DataSource;

/* DAO Support Interface */
public interface DAO {
	
	public void setDataSource(DataSource ds);
	
	public void insert(String hostname, String eid, Integer duration, String startTime);
	
	public RentDate getStudent(Integer id);
	
	public List<RentDate> listAllDate();
	
	public void delete(Integer id);
	
	public void update(String hostname, String eid, Integer duration, String startTime, Integer id);
}	
