package com.registration;

import java.util.List;
import javax.sql.DataSource;

/* DAO Support Interface */
public interface StudentDAO {
	
	public void setDataSource(DataSource ds);
	
	public void create(String name, Integer age);
	
	public Student getStudent(Integer id);
	
	public List<Student> listStudents();
	
	public void delete(Integer id);
	
	public void update(Integer id, Integer age);
	
	public void update(Integer id, String name);
	
	public void update(Integer id, String name, Integer age, String time);
}	
