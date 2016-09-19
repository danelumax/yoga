/*
 * DiaSessionDataDBUtil.cpp
 *
 *  Created on: Sep 13, 2016
 *      Author: eliwech
 */

#include "DiaSessionDataDBUtil.h"
#include "ResultSet.h"
#include "SearchOption.h"
#include "Modification.h"
#include "DBServiceProvider.h"
#include "VernalNdbTransaction.h"
#include <iostream>

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
		Dao* dao = db->getDao(transaction);
	    dao->insert(modify);
	    transaction->commit();
	}

	return 0;
}

int DiaSessionDataDBUtil::findSessionDatafromDB()
{
	std::string table = "api_simple";
	SearchOption querySession(table);
	querySession.addCriteria(SEARCH_OPTION_QUERY_TYPE, SearchOption::CT_EQ, SEARCH_OPTION_QUERY_TYPE_SINGLE_PK);
	querySession.addCriteria("ATTR2", SearchOption::CT_EQ, "1");
	ResultSet record(table);
	DBServiceProvider* db = DBServiceProvider::getInstance();
	db->find(querySession, record);
}


