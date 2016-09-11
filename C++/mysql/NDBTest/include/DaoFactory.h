/*
 * DaoFactory.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef DAOFACTORY_H_
#define DAOFACTORY_H_

#include "Transaction.h"

class DaoFactory
{
public:
	virtual ~DaoFactory();
	static DaoFactory* getInstance();
	static void destory();
	Transaction* startTransaction();
private:
	DaoFactory();
	static DaoFactory* _instance;
};

#endif /* DAOFACTORY_H_ */
