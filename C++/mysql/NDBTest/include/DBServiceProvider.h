/*
 * DBServiceProvider.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef DBSERVICEPROVIDER_H_
#define DBSERVICEPROVIDER_H_

#include "NdbDao.h"
#include "Modification.h"
#include "Transaction.h"

class DBServiceProvider
{
public:
	virtual ~DBServiceProvider();
	static DBServiceProvider* getInstance();
	static void destory();
	int insert(Modification& record);
	NdbDao* getDao(Transaction* transaction = NULL);
	Transaction* startTransaction();
private:
	DBServiceProvider();
	static DBServiceProvider* _instance;
};

#endif /* DBSERVICEPROVIDER_H_ */
