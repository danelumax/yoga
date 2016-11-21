package com.transaction.declarative;

import java.util.List;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.dao.DataAccessException;

public class StudentDAOImpl implements StudentDAO{
	final String InsertStudentSQL = "insert into Student (name, age) values (?, ?)";
	final String InsertMarkSQL  = "insert into Marks(sid, marks, year) values (?, ?, ?)";
	final String SelectStudentSQL = "select max(id) from Student";
	
	private JdbcTemplate jdbcTemplateObject;
	
	@Override
	public void setDataSource(DataSource dataSource) {
		this.jdbcTemplateObject = new JdbcTemplate(dataSource);
	}
	@Override
	public void create(String name, Integer age, Integer marks, Integer year) {
		try {
			this.jdbcTemplateObject.update(InsertStudentSQL, name, age);
			int sid = this.jdbcTemplateObject.queryForObject(SelectStudentSQL, Integer.class);
			this.jdbcTemplateObject.update(InsertMarkSQL, sid, marks, year);
			System.out.println("Created Name = " + name + ", Age = " + age);
			/* if throw exception, transaction will rollback */
			throw new RuntimeException("I want to thow a exception, and rollback transaction ...") ;
		} catch (DataAccessException e) {
	        System.out.println("Error in creating record, rolling back");
	        throw e;
		}
	}
	@Override
	public List<StudentMarks> listStudents() {
		String SQL = "select * from Student, Marks where Student.id=Marks.sid";
		List <StudentMarks> studentMarks=jdbcTemplateObject.query(SQL, new StudentMarkMapper());
		return studentMarks;
	}	
	
}
