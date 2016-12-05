package com.mysql;

public class MainApp {

	public static void main(String[] args) throws Exception {
		final String dropSQL = "drop table if exists my_test";
		final String createSQL = "create table my_test ( " +
				  				 "test_id int auto_increment primary key, " +
				  				 "test_name varchar(255))";
		final String insertSQL = "insert into my_test(test_name) values('Liwei')";
		final String selectSQL = "select * from my_test";
		
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
