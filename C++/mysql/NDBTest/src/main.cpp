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

/**************************************************************************
 * Using 5 transactions, insert 10 tuples in table: (0,0),(1,1),...,(9,9) *
 **************************************************************************/
static void do_insert(Ndb* myNdb)
{
	const NdbDictionary::Dictionary* myDict= myNdb->getDictionary();
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	if (myTable == NULL)
		APIERROR(myDict->getNdbError());

	for (int i = 0; i < 5; i++)
	{
		NdbTransaction *myTransaction= myNdb->startTransaction();
		if (myTransaction == NULL)
			APIERROR(myNdb->getNdbError());
  
		NdbOperation *myOperation= myTransaction->getNdbOperation(myTable);
		if (myOperation == NULL)
			APIERROR(myTransaction->getNdbError());
  
		myOperation->insertTuple();
		myOperation->equal("ATTR1", i);
		myOperation->setValue("ATTR2", i);

		myOperation= myTransaction->getNdbOperation(myTable);
		if (myOperation == NULL)
			APIERROR(myTransaction->getNdbError());

		myOperation->insertTuple();
		myOperation->equal("ATTR1", i+5);
		myOperation->setValue("ATTR2", i+5);
  
		NdbUtils::executeNdbTransaction(myTransaction,
										NdbTransaction::Commit,
										NdbOperation::AbortOnError);
		myNdb->closeTransaction(myTransaction);
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
  
		myOperation->updateTuple();
		myOperation->equal( "ATTR1", i );
		myOperation->setValue( "ATTR2", i+10);
  
		NdbUtils::executeNdbTransaction(myTransaction,
										NdbTransaction::Commit,
										NdbOperation::AbortOnError);
  
		myNdb->closeTransaction(myTransaction);
	}
}

/*************************************************
 * Delete one tuple (the one with primary key 3) *
 *************************************************/
static void do_delete(Ndb* myNdb)
{
	const NdbDictionary::Dictionary* myDict= myNdb->getDictionary();
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	if (myTable == NULL)
		APIERROR(myDict->getNdbError());

	NdbTransaction *myTransaction= myNdb->startTransaction();
	if (myTransaction == NULL)
		APIERROR(myNdb->getNdbError());

	NdbOperation *myOperation= myTransaction->getNdbOperation(myTable);
	if (myOperation == NULL)
		APIERROR(myTransaction->getNdbError());

	myOperation->deleteTuple();
	myOperation->equal( "ATTR1", 3 );

	NdbUtils::executeNdbTransaction(myTransaction,
									NdbTransaction::Commit,
									NdbOperation::AbortOnError);

	myNdb->closeTransaction(myTransaction);
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
  
		myOperation->readTuple(NdbOperation::LM_Read);
		myOperation->equal("ATTR1", i);

		NdbRecAttr *myRecAttr= myOperation->getValue("ATTR2", NULL);
		if (myRecAttr == NULL)
			APIERROR(myTransaction->getNdbError());
  
		NdbUtils::executeNdbTransaction(myTransaction,
										NdbTransaction::Commit,
										NdbOperation::DefaultAbortOption);
		//if(myTransaction->execute( NdbTransaction::Commit ) == -1)
		//	APIERROR(myTransaction->getNdbError());
  
		if (myTransaction->getNdbError().classification == NdbError::NoDataFound)
		{
			if (i == 3)
				std::cout << "Detected that deleted tuple doesn't exist!" << std::endl;
			else
				APIERROR(myTransaction->getNdbError());
		}

		if (i != 3)
		{
			printf(" %2d    %2d\n", i, myRecAttr->u_32_value());
		}
		myNdb->closeTransaction(myTransaction);
	}
}

//static void run_application(MYSQL &mysql, Ndb_cluster_connection* cluster_connection)
static void run_application(MYSQL &mysql)
{
	/********************************************
	 * Connect to database via mysql-c          *ndb_examples
	 ********************************************/
	mysql_query(&mysql, "CREATE DATABASE ndb_examples");
	if (mysql_query(&mysql, "USE ndb_examples") != 0)
		MYSQLERROR(mysql);
	create_table(mysql);

	/********************************************
	 * Connect to database via NdbApi           *
	 ********************************************/
	Ndb* myNdb = NdbClusterManager::getInstance()->getNdb();

	/*
	 * Do different operations on database
	 */
	do_insert(myNdb);
	do_update(myNdb);
	do_delete(myNdb);
	do_read(myNdb);

}


int main(int argc, char** argv)
{
    // connect to mysql server and cluster and run application
    NdbClusterManager::getInstance()->connectToCluster();

    // connect to mysql server
    MYSQL mysql;
    if ( !mysql_init(&mysql) ) {
    	std::cout << "mysql_init failed\n";
    	_exit(-1);
    }
    if ( !mysql_real_connect(&mysql, "localhost", "root", "rootroot", "test", 0, NULL, 0) )
    	MYSQLERROR(mysql);

    run_application(mysql);

    NdbClusterManager::destory();

    return 0;
}
