package com.registration;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

import com.pojo.RentData;

/* user-defined query result, just for callback */
public class StudentMapper implements RowMapper<RentData> {
	@Override
	public RentData mapRow(ResultSet rs, int rowNum) throws SQLException {
		RentData date = new RentData();
		date.setId(rs.getInt("id"));
		date.setHostName(rs.getString("hostname"));
		date.setEid(rs.getString("eid"));
		date.setDuration(rs.getInt("duration"));
		date.setStartTime(rs.getString("startTime"));
		
		return date;
	}
}
