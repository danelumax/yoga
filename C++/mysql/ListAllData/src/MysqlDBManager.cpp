/*
 * MysqlDBManager.cpp
 *
 *  Created on: Sep 5, 2016
 *      Author: eliwech
 */

#include "MysqlDBManager.h"
#include <iostream>
#include <string>

MysqlDBManager* MysqlDBManager::_instance = NULL;

MysqlDBManager::MysqlDBManager()
	:_mysql(NULL)
{
}

MysqlDBManager::~MysqlDBManager()
{
}

MysqlDBManager* MysqlDBManager::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new MysqlDBManager();
	}

	return _instance;
}

void MysqlDBManager::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}

int MysqlDBManager::initMysql()
{
	int ret = 0;
	_mysql = mysql_init(NULL);
	if (NULL == _mysql)
	{
		ret = -1;
		std::cout << "init mysql failed" << std::endl;
	}

	return ret;
}

int MysqlDBManager::connectMysql()
{
	int ret = 0;
	if (NULL == mysql_real_connect(_mysql, "localhost", "root", "rootroot", "test", 3306, NULL, 0))
	{
		ret = -1;
		std::cout << "connect to mysql failed" << std::endl;
	}

	return ret;
}

void MysqlDBManager::listAllData()
{
    MYSQL_RES *result = NULL;
    MYSQL_FIELD *field = NULL;
    std::string sql = "select id,name from t1;";
    mysql_query(_mysql, sql.c_str());
    result = mysql_store_result(_mysql);
    int rowcount = mysql_num_rows(result);
    std::cout << "rowcount:" << rowcount << std::endl;
    int fieldcount = mysql_num_fields(result);
    std::cout << "fieldcount:" << fieldcount << std::endl;
    for(int i = 0; i < fieldcount; i++)
    {
     field = mysql_fetch_field_direct(result,i);
     std::cout << field->name << "\t\t";
    }
    std::cout << std::endl;
    MYSQL_ROW row = NULL;
    row = mysql_fetch_row(result);
    while(NULL != row)
    {
     for(int i=0; i<fieldcount; i++)
     {
    	 std::cout << row[i] << "\t\t";
     }
     std::cout << std::endl;
     row = mysql_fetch_row(result);
    }
    mysql_close(_mysql);
}
