/*
 * DaoFactory.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef DAOFACTORY_H_
#define DAOFACTORY_H_

#include "Transaction.h"
#include <vector>
#include "Dao.h"
#include "NdbDao.h"

class DaoFactory
{
public:
	virtual ~DaoFactory();
	static DaoFactory* getInstance();
	static void destory();
	Transaction* startTransaction();
	void closeTransaction(Transaction* transaction);
	Dao* factoryDao(std::string key, Transaction* transaction = NULL);
private:
	DaoFactory();
	static DaoFactory* _instance;
	std::vector<Transaction*> _daoTransaction;
};

#endif /* DAOFACTORY_H_ */
