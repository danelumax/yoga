package com.jdbctemplate;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

/* user-defined query result, just for callback */
public class StudentMapper implements RowMapper<Student> {
	@Override
	public Student mapRow(ResultSet rs, int rowNum) throws SQLException {
		Student student = new Student();
		student.setId(rs.getInt("id"));
		student.setName(rs.getString("name") + "_yoga");
		student.setAge(rs.getInt("age"));
		return student;
	}
}
