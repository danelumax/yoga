package com.registration;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

/* user-defined query result, just for callback */
public class StudentMapper implements RowMapper<RentDate> {
	@Override
	public RentDate mapRow(ResultSet rs, int rowNum) throws SQLException {
		RentDate date = new RentDate();
		date.setId(rs.getInt("id"));
		date.setHostName(rs.getString("hostname"));
		date.setEid(rs.getString("id"));
		date.setDuration(rs.getInt("duration"));
		date.setStartTime(rs.getString("startTime"));
		return date;
	}
}
