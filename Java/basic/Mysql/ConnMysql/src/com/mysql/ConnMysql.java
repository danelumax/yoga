package com.mysql;

import java.sql.DriverManager;
import java.sql.ResultSet;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

public class ConnMysql {

	public static void main(String[] args) throws Exception {
		Class.forName("com.mysql.jdbc.Driver");
		try(
			Connection conn = (Connection) DriverManager.getConnection(
				"jdbc:mysql://127.0.0.1:33006/test", "root", "rootroot");
			Statement stmt = (Statement) conn.createStatement();
			ResultSet rs = stmt.executeQuery("select * from Student");) 
		{
			while(rs.next()) {
				System.out.println(rs.getInt(1) + "\t"
					+ rs.getString(2) + "\t"
					+ rs.getString(3));
			}
		}
	}
}
