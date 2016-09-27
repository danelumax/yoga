/*
 *  ndbapi_simple.cpp: Using synchronous transactions in NDB API
 *
 *  Correct output from this program is:
 *
 *  ATTR1 ATTR2
 *    0    10
 *    1     1
 *    2    12
 *  Detected that deleted tuple doesn't exist!
 *    4    14
 *    5     5
 *    6    16
 *    7     7
 *    8    18
 *    9     9
 *
 */

#include <mysql.h>
#include <mysqld_error.h>
#include <NdbApi.hpp>
#include <stdio.h>
#include <iostream>

#include "NdbUtils.h"
#include "NdbClusterManager.h"
#include "NdbOperationTransaction.h"
#include "DiaSessionDataDBUtil.h"

#define PRINT_ERROR(code,msg) \
  std::cout << "Error in " << __FILE__ << ", line: " << __LINE__ \
            << ", code: " << code \
            << ", msg: " << msg << "." << std::endl
#define MYSQLERROR(mysql) {PRINT_ERROR(mysql_errno(&mysql),mysql_error(&mysql)); _exit(-1);}
#define APIERROR(error) {PRINT_ERROR(error.code,error.message); _exit(-1);}


/*********************************************************
 * Create a table named api_simple if it does not exist *
 *********************************************************/
static void create_table(MYSQL &mysql)
{
	/* ATTR1 is primary key. 1,2,3,4,5,6,7,8,9,10 */
	while (mysql_query(&mysql,
					   "CREATE TABLE api_simple (ATTR1 INT UNSIGNED NOT NULL PRIMARY KEY, ATTR2 INT UNSIGNED NOT NULL) ENGINE=NDB"))
	{
		if (mysql_errno(&mysql) == ER_TABLE_EXISTS_ERROR)
		{
			std::cout << "MySQL Cluster already has example table: api_simple. "
					  << "Dropping it..." << std::endl;
			mysql_query(&mysql, "DROP TABLE api_simple");
		}
		else
		{
			MYSQLERROR(mysql);
		}
	}
}

/*****************************************************************
 * Update the second attribute in half of the tuples (adding 10) *
 *****************************************************************/
static void do_update(Ndb* myNdb)
{
	const NdbDictionary::Dictionary* myDict= myNdb->getDictionary();
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	if (myTable == NULL)
		APIERROR(myDict->getNdbError());

	for (int i = 0; i < 10; i+=2)
	{
		NdbTransaction *myTransaction= myNdb->startTransaction();
		if (myTransaction == NULL)
			APIERROR(myNdb->getNdbError());
  
		NdbOperation *myOperation= myTransaction->getNdbOperation(myTable);
		if (myOperation == NULL)
			APIERROR(myTransaction->getNdbError());
  
		/* This method defines the NdbOperation as an UPDATE operation.
		 * When the NdbTransaction::execute() method is invoked,
		 * the operation updates a tuple found in the table.
		 * */
		myOperation->updateTuple();
		myOperation->equal( "ATTR1", i );
		/*(0,10)(1,1)(2,12)(3,3)(4,14) ... (8,18)(9,9)*/
		myOperation->setValue( "ATTR2", i+10);
  
		NdbUtils::executeNdbTransaction(myTransaction,
										NdbTransaction::Commit,
										NdbOperation::AbortOnError);
  
		myNdb->closeTransaction(myTransaction);
	}
}

/*****************************
 * Read and print all tuples *
 *****************************/
static void do_read(Ndb* myNdb)
{
	const NdbDictionary::Dictionary* myDict= myNdb->getDictionary();
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	if (myTable == NULL)
		APIERROR(myDict->getNdbError());

	std::cout << "ATTR1 ATTR2" << std::endl;

	for (int i = 0; i < 10; i++)
	{
		NdbTransaction *myTransaction= myNdb->startTransaction();
		if (myTransaction == NULL)
			APIERROR(myNdb->getNdbError());
  
		NdbOperation *myOperation= myTransaction->getNdbOperation(myTable);
		if (myOperation == NULL)
			APIERROR(myTransaction->getNdbError());
  
		/* a READ operation */
		myOperation->readTuple(NdbOperation::LM_Read);
		/* find key */
		myOperation->equal("ATTR1", i);

		/* get what, but wait for "execute" */
		//NdbUtils::prepareNdbOperationQuerySpace
		NdbRecAttr *myRecAttr= myOperation->getValue("ATTR2", NULL);
		if (myRecAttr == NULL)
			APIERROR(myTransaction->getNdbError());
  
		/* after execute, myOperation take effect and myRecAttr get value */
		NdbUtils::executeNdbTransaction(myTransaction,
										NdbTransaction::Commit,
										NdbOperation::DefaultAbortOption);
  
		if (myTransaction->getNdbError().classification == NdbError::NoDataFound)
		{
			if (i == 5)
				std::cout << "Detected that deleted tuple doesn't exist!" << std::endl;
			else
				APIERROR(myTransaction->getNdbError());
		}

		if (i != 5)
		{
			printf(" %2d    %2d\n", i, myRecAttr->u_32_value());
		}
		myNdb->closeTransaction(myTransaction);
	}
}

static void run_application()
{
	Ndb* ndb = NdbClusterManager::getInstance()->getNdb();

	std::cout << "\ninsert" << std::endl;
	DiaSessionDataDBUtil::insertSessionDataToDB();
	DiaSessionDataDBUtil::findSessionDatafromDB();

	std::cout << "\nupdate" << std::endl;
	do_update(ndb);

	std::cout << "\ndelete" << std::endl;
	DiaSessionDataDBUtil::deleteSessionDataInDB();

	std::cout << "\nread" << std::endl;
	//do_read(ndb);
	DiaSessionDataDBUtil::findSessionDatafromDB();

	//std::cout << "\nfind" << std::endl;
	//DiaSessionDataDBUtil::findSessionDatafromDB();
}

void createMysql()
{
	/* connect to mysql server */
    MYSQL mysql;
    if (!mysql_init(&mysql))
    {
    	std::cout << "mysql_init failed\n";
    	_exit(-1);
    }

    if ( !mysql_real_connect(&mysql, "localhost", "root", "rootroot", "test", 0, NULL, 0) )
    {
    	MYSQLERROR(mysql);
    }

	mysql_query(&mysql, "CREATE DATABASE ndb_examples");

	if (mysql_query(&mysql, "USE ndb_examples") != 0)
	{
		MYSQLERROR(mysql);
	}

	create_table(mysql);
}


int main(int argc, char** argv)
{
	NdbClusterManager::getInstance()->run();

	createMysql();

    run_application();

    NdbClusterManager::destory();

    return 0;
}
