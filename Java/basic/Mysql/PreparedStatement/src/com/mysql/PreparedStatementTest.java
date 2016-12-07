package com.mysql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

import com.mysql.jdbc.PreparedStatement;

public class PreparedStatementTest {
	private String driver;
	private String url;
	private String user;
	private String pass;

	public PreparedStatementTest() {
		this.driver = "com.mysql.jdbc.Driver";
		this.url = "jdbc:mysql://127.0.0.1:33006/test";
		this.user = "root";
		this.pass = "rootroot";
	}
	
	public void insertUseStatement() throws Exception {
		long start = System.currentTimeMillis();
		Class.forName(this.driver);
		try(
			Connection conn = DriverManager.getConnection(this.url, this.user, this.pass);
			Statement stmt = (Statement) conn.createStatement()) {
			for (int i=0; i<100; i++) {
				stmt.execute("insert into student_table values (null, 'name" + i + "' ,1)");
			}
			System.out.println("Statement consume: " + (System.currentTimeMillis()-start) + " ms");
		}
	}
	
	public void insertUsePrepare() throws Exception {
		long start = System.currentTimeMillis();
		Class.forName(this.driver);
		try(
			Connection conn = DriverManager.getConnection(this.url, this.user, this.pass);
			PreparedStatement pstmt = (PreparedStatement) conn.prepareStatement(
				"insert into student_table values(null, ?, 1)")) {
			for (int i=0; i<100; i++) {
				pstmt.setString(1, "name" + i);
				pstmt.executeUpdate();
			}
			System.out.println("PreparedStatement consume: " + (System.currentTimeMillis()-start) + " ms");
		}
	}
}
