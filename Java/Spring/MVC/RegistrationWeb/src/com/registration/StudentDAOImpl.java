package com.registration;

import java.util.List;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;


public class StudentDAOImpl implements StudentDAO{
	final String InsertSQL = "insert into Student (name, age, RegistrationTime) values (?, ?, ?)";
	final String SingleQuerySQL = "select * from Student where id = ?";
	final String ListAllSQL = "select * from Student";
	final String SingleDeleteSQL = "delete from Student where id = ?";
	final String UpdateAgeSQL = "update Student set age = ? where id = ?";
	final String UpdateNameSQL = "update Student set name = ? where id = ?";
	final String UpdateStudentSQL = "update Student set name=?, age=?, RegistrationTime=? where id = ?";
	
	private DataSource dataSource;
	private JdbcTemplate jdbcTemplateObject;
	
	@Override
	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
		this.jdbcTemplateObject = new JdbcTemplate(dataSource);
	}
	@Override
	public void insert(String name, Integer age, String time) {
		this.jdbcTemplateObject.update(InsertSQL, name, age, time);
		System.out.println("Create Record Name = " + name + ", Age = " + age  + ", Time = " + time);
		return;
	}
	@Override
	public Student getStudent(Integer id) {
		Student student = this.jdbcTemplateObject.queryForObject(SingleQuerySQL, 
						  new Object[]{id}, new StudentMapper());
		return student;
	}
	@Override
	public List<Student> listStudents() {
		List<Student> students = this.jdbcTemplateObject.query(ListAllSQL,
								 new StudentMapper());
		return students;
	}
	@Override
	public void delete(Integer id) {
		this.jdbcTemplateObject.update(SingleDeleteSQL, id);
		System.out.println("Deleted Record with ID = " + id);
		return;
	}
	@Override
	public void update(Integer id, Integer age) {
		this.jdbcTemplateObject.update(UpdateAgeSQL, age, id);
		System.out.println("Update Record with ID = " + id);
		return;
	}
	
	@Override
	public void update(Integer id, String name) {
		this.jdbcTemplateObject.update(UpdateNameSQL, name, id);
		System.out.println("Update Record with ID = " + id);
		return;
	}
	
	@Override
	public void update(Integer id, String name, Integer age, String time) {
		this.jdbcTemplateObject.update(UpdateStudentSQL, name, age, time, id);
		System.out.println("Update Record with ID = " + id);
		return;
	}
}
