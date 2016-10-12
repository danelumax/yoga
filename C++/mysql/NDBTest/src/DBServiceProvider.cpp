/*
 * DBServiceProvider.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "DBServiceProvider.h"
#include <iostream>
#include "NdbDao.h"
#include "DaoFactory.h"

DBServiceProvider* DBServiceProvider::_instance = NULL;

DBServiceProvider::DBServiceProvider()
{
}

DBServiceProvider::~DBServiceProvider()
{
}

DBServiceProvider* DBServiceProvider::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new DBServiceProvider();
	}

	return _instance;
}

void DBServiceProvider::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* single query */
int DBServiceProvider::find(SearchOption & searchOption, ResultSet & record)
{
	std::vector<ResultSet> records;
	int ret = find(searchOption, records);
	if (ret == RE_DAO_SUC)
	{
		if (records.size() > 0)
		{
			record = records[0];
		}
		else
		{
			ret = RE_DAO_ERROR;
		}
	}

	return ret;
}

int DBServiceProvider::find(SearchOption & searchOption, std::vector<ResultSet> & records)
{
	Dao* dao = getDao("DAO_NDB");
	if (!dao)
	{
		return RE_DAO_ERROR;
	}

	int ret = dao->find(searchOption, records);

	return ret;
}

int DBServiceProvider::insert(Modification& record)
{
	Dao* dao = getDao("DAO_NDB");
	dao->insert(record);

	return 0;
}

Dao* DBServiceProvider::getDao(const std::string& key, Transaction* transaction)
{
	return DaoFactory::getInstance()->factoryDao(key, transaction);
}

Transaction* DBServiceProvider::startTransaction()
{
	return DaoFactory::getInstance()->startTransaction();
}

void DBServiceProvider::closeTransaction(Transaction* transaction)
{
	DaoFactory::getInstance()->closeTransaction(transaction);
}
