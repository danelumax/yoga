/*
 * DiaSessionDataDBUtil.cpp
 *
 *  Created on: Sep 13, 2016
 *      Author: eliwech
 */

#include "DiaSessionDataDBUtil.h"
#include <iostream>
#include <sstream>
#include "SearchOption.h"
#include "Modification.h"
#include "DBServiceProvider.h"
#include "VernalNdbTransaction.h"

/**************************************************************************
 * insert 10 tuples in table: (0,0),(1,1),...,(9,9) *
 **************************************************************************/
int DiaSessionDataDBUtil::insertSessionDataToDB()
{
	for (int i = 0; i < 10; i++)
	{
		Modification modify("api_simple");
		modify.addValue("ATTR1", i);
		//modify.addValue("ATTR2", i);
		DBServiceProvider* db = DBServiceProvider::getInstance();

		Transaction* transaction = db->startTransaction();
		Dao* dao = db->getDao("DAO_NDB", transaction);
	    dao->insert(modify);
	    transaction->commit();
	    db->closeTransaction(transaction);

	    //db->insert(modify);
	}

	return 0;
}

int DiaSessionDataDBUtil::findSessionDatafromDB()
{
	int ret = 0;
	std::string table = "api_simple";

	std::cout << "ATTR1 ATTR2" << std::endl;
	for (int i = 0; i < 10; i++)
	{
		SearchOption querySession(table);

		std::ostringstream oss;
		oss << i;

		querySession.addCriteria(SEARCH_OPTION_QUERY_TYPE, SearchOption::CT_EQ, SEARCH_OPTION_QUERY_TYPE_SINGLE_PK);
		querySession.addCriteria("ATTR1", SearchOption::CT_EQ, oss.str());
		ResultSet record;
		DBServiceProvider* db = DBServiceProvider::getInstance();
		ret = db->find(querySession, record);
		if (RE_DAO_NO_DATA == ret)
		{
			std::cout << "DiaSessionDataDBUtil::findSessionDatafromDB Can't find in DB" << std::endl;
		}
		if (RE_DAO_SUC != ret)
		{
			std::cout << "DiaSessionDataDBUtil::findSessionDatafromDB Find failed" << std::endl;
		}

		std::cout << "  " << i << "    ";
		sinkValueForSessionTable(record);
	}

	return 0;
}

int DiaSessionDataDBUtil::deleteSessionDataInDB()
{
	int ret = 0;

	DBServiceProvider* db = DBServiceProvider::getInstance();
	Transaction* transaction = db->startTransaction();
	Dao* dao = db->getDao("DAO_NDB", transaction);

	std::string table = "api_simple";
	SearchOption querySession(table);
	querySession.addCriteria(SEARCH_OPTION_QUERY_TYPE, SearchOption::CT_EQ, SEARCH_OPTION_QUERY_TYPE_SINGLE_PK);
	querySession.addCriteria("ATTR1", SearchOption::CT_EQ, "5");
	ret = dao->remove(querySession);
	if (ret!=RE_DAO_SUC && ret!=RE_DAO_NO_DATA)
	{
		std::cout << "DiaSessionDataDBUtil::Delete data from database failed" << std::endl;
		return -1;
	}

    ret = transaction->commit();

    db->closeTransaction(transaction);

	return 0;
}

void DiaSessionDataDBUtil::sinkValueForSessionTable(ResultSet& record)
{
	std::map<std::string, std::string> test = record.getValues();
	std::map<std::string, std::string>::iterator iter = test.find("ATTR2");

	std::cout << iter->second << std::endl;
}


