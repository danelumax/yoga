package com.mysql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;

public class ExecuteSQL {
	private String driver;
	private String url;
	private String user;
	private String pass;

	public ExecuteSQL() {
		this.driver = "com.mysql.jdbc.Driver";
		this.url = "jdbc:mysql://127.0.0.1:33006/test";
		this.user = "root";
		this.pass = "rootroot";
	}
	
	public void executeSql(String sql) throws Exception {
		 Class.forName(this.driver);
		 try(
			Connection conn = DriverManager.getConnection(this.url, this.user, this.pass);
			Statement stmt = (Statement) conn.createStatement()) {
			boolean hasResultSet = stmt.execute(sql);
			/* if get ResultSet(select) */
			if (hasResultSet) {
				try(ResultSet rs = stmt.getResultSet()) {
					/* Column count is stored in ResultSetMetaData */
					ResultSetMetaData rsmd = rs.getMetaData();
					int columnCount = rsmd.getColumnCount();
					while (rs.next()) {
						for (int i=0; i<columnCount; i++) {
							System.out.print(rs.getString(i+1) + "\t");
						}
						System.out.print("\n");
					}
				}
			} else {
				System.out.println("This SQL will impact " + stmt.getUpdateCount() + " records");
			}
		 }
	}
}
