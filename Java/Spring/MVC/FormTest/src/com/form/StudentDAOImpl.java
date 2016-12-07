package com.form;

import java.util.List;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;


public class StudentDAOImpl implements StudentDAO{
	final String InsertSQL = "insert into Student (name, age) values (?, ?)";
	final String SingleQuerySQL = "select * from Student where id = ?";
	final String ListAllSQL = "select * from Student";
	final String SingleDeleteSQL = "delete from Student";
	final String UpdateSQL = "update Student set age = ? where id = ?";
	
	private DataSource dataSource;
	private JdbcTemplate jdbcTemplateObject;
	
	@Override
	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
		this.jdbcTemplateObject = new JdbcTemplate(dataSource);
	}
	@Override
	public void create(String name, Integer age) {
		this.jdbcTemplateObject.update(InsertSQL, name, age);
		System.out.println("Create Record Name = " + name + "Age = " + age);
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
		List<Student> stduents = this.jdbcTemplateObject.query(ListAllSQL,
								 new StudentMapper());
		return stduents;
	}
	@Override
	public void delete(Integer id) {
		this.jdbcTemplateObject.update(SingleDeleteSQL, id);
		System.out.println("Deleted Record with ID = " + id);
		return;
	}
	@Override
	public void update(Integer id, Integer age) {
		this.jdbcTemplateObject.update(UpdateSQL, age, id);
		System.out.println("Update Record with ID = " + id);
		return;
	}
}
