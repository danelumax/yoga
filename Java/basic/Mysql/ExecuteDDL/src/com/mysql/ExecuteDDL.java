package com.mysql;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.DriverManager;
import java.util.Properties;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

public class ExecuteDDL {
	
	private Connection conn;
	private Statement stmt;

	private String driver;
	private String url;
	private String user;
	private String pass;

	public ExecuteDDL() {
		this.driver = "com.mysql.jdbc.Driver";
		this.url = "jdbc:mysql://127.0.0.1:33006/test";
		this.user = "root";
		this.pass = "rootroot";
	}
	public Statement getStmt() {
		return stmt;
	}

	public void setStmt(Statement stmt) {
		this.stmt = stmt;
	}
	
	public void initMysql() throws Exception {
		Class.forName(this.driver);
		this.conn = (Connection) DriverManager.getConnection(this.url, this.user, this.pass);
		this.stmt = (Statement) this.conn.createStatement();
	}
	
	public static void main(String[] args) throws Exception {
		String createTabSQL = "create table jdbc_test ( " +
							  "jdbc_id int auto_increment primary key, " +
							  "jdbc_name varchar(255), " +
							  "jdbc_desc text);";
		String descTabSQL = "desc jdbc_test";
		String deleteTabQL = "drop table jdbc_test";
		
		ExecuteDDL ed = new ExecuteDDL();
		ed.initMysql();
		
		ed.getStmt().executeUpdate(createTabSQL);
		System.out.println("Create Table Successfully !");
		ed.getStmt().executeUpdate(deleteTabQL);
		System.out.println("Drop Table Successfully !");
	}

}
