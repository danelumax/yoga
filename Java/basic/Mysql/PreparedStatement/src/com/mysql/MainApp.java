package com.mysql;

public class MainApp {

	public static void main(String[] args) throws Exception {
		
		PreparedStatementTest pt = new PreparedStatementTest();
		pt.insertUseStatement();
		pt.insertUsePrepare();
	}
}
