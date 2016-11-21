package com.transaction.declarative;

import java.util.List;
import javax.sql.DataSource;

/* DAO Support Interface */
public interface StudentDAO {
	
	public void setDataSource(DataSource ds);
	
	public void create(String name, Integer age, Integer marks, Integer year);
	
	public List<StudentMarks> listStudents();
}	
