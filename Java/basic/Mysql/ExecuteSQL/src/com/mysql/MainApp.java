package com.mysql;

public class MainApp {

	public static void main(String[] args) throws Exception {
		final String dropSQL = "drop table if exists student_table";
		final String createSQL = "create table student_table ( " +
				  				 "student_id int auto_increment primary key, " +
				  				 "student_name varchar(255)," +
				  				 "student_age int)";
		final String insertSQL = "insert into student_table(student_name) values('Liwei')";
		final String selectSQL = "select * from student_table";
		
		ExecuteSQL es = new ExecuteSQL();
		
		System.out.println("----- Delete Existed Table -----");
		es.executeSql(dropSQL);
		
		System.out.println("----- Create Table -----");
		es.executeSql(createSQL);
		
		System.out.println("----- Insert Data -----");
		es.executeSql(insertSQL);
		
		System.out.println("----- Query Data -----");
		es.executeSql(selectSQL);
	}
}
