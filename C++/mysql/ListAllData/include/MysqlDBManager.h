/*
 * MysqlDBManager.h
 *
 *  Created on: Sep 5, 2016
 *      Author: eliwech
 */

#ifndef MYSQLDBMANAGER_H_
#define MYSQLDBMANAGER_H_

#include <mysql.h>

class MysqlDBManager
{
public:
	~MysqlDBManager();
	static MysqlDBManager* getInstance();
	static void destory();
	int initMysql();
	int connectMysql();
	void listAllData();

private:
	MysqlDBManager();
	static MysqlDBManager* _instance;
	MYSQL *_mysql;
};

#endif /* MYSQLDBMANAGER_H_ */
