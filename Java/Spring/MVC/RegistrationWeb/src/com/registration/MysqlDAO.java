package com.registration;

import java.util.List;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;


public class MysqlDAO implements DAO{
	final String TableName = "MachineRent";
	final String InsertSQL = "insert into " + TableName + " (hostname, eid, duration, startTime) values (?, ?, ?, ?)";
	final String SingleQuerySQL = "select * from " + TableName + " where id = ?";
	final String ListAllSQL = "select * from " + TableName;
	final String SingleDeleteSQL = "delete from " + TableName + " where id = ?";
	final String UpdateStudentSQL = "update " + TableName + " set hostname=?, eid=?, duration=?, startTime=? where id = ?";
	
	private DataSource dataSource;
	private JdbcTemplate jdbcTemplateObject;
	
	@Override
	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
		this.jdbcTemplateObject = new JdbcTemplate(dataSource);
	}
	@Override
	public void insert(String hostname, String eid, Integer duration, String startTime) {
		this.jdbcTemplateObject.update(InsertSQL, hostname, eid, duration, startTime);
		System.out.println("Create Record Hostname = " + hostname + ", eid = " + eid  + ", Duration = " + duration + ", StartTime = " + startTime);
	}
	@Override
	public RentData getStudent(Integer id) {
		RentData student = this.jdbcTemplateObject.queryForObject(SingleQuerySQL, 
						  new Object[]{id}, new StudentMapper());
		return student;
	}
	@Override
	public List<RentData> listAllDate() {
		List<RentData> students = this.jdbcTemplateObject.query(ListAllSQL, new StudentMapper());
		return students;
	}
	@Override
	public void delete(Integer id) {
		this.jdbcTemplateObject.update(SingleDeleteSQL, id);
		System.out.println("Deleted Record with ID = " + id);
	}	
	@Override
	public void update(String hostname, String eid, Integer duration, String startTime, Integer id) {
		this.jdbcTemplateObject.update(UpdateStudentSQL,  hostname, eid, duration, startTime, id);
		System.out.println("Update Record with ID = " + id);
	}
}
