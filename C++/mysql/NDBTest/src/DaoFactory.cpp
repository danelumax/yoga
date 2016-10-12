/*
 * DaoFactory.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "DaoFactory.h"
#include <iostream>
#include "VernalNdbTransaction.h"

DaoFactory* DaoFactory::_instance = NULL;

DaoFactory::DaoFactory()
{
}

DaoFactory::~DaoFactory()
{
	std::vector<Transaction*>::iterator iter = _daoTransaction.begin();
	for (; iter!=_daoTransaction.end(); ++iter)
	{
		Transaction* trans = (*iter);
		delete trans;
	}
	_daoTransaction.clear();
}

DaoFactory* DaoFactory::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new DaoFactory;
	}

	return _instance;
}

void DaoFactory::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}

Transaction* DaoFactory::startTransaction()
{
	Transaction* transaction = new VernalNdbTransaction();
	if (transaction->start() != 0)
	{
		delete transaction;
		transaction = NULL;
	}

	_daoTransaction.push_back(transaction);

	return transaction;
}

void DaoFactory::closeTransaction(Transaction* transaction)
{
	if (!transaction)
	{
		std::cout << "input transaction is null" << std::endl;
		return;
	}

	std::vector<Transaction*>::iterator iter = _daoTransaction.begin();
	for(; iter!=_daoTransaction.end(); ++iter)
	{
		Transaction* trans = (*iter);
		if (trans == transaction)
		{
			delete trans;
			_daoTransaction.erase(iter);
			break;
		}
	}
}

Dao *DaoFactory::factoryDao(std::string key, Transaction* transaction)
{
	if ("DAO_NDB" == key)
	{
		NdbDao* ndbDao = new NdbDao(transaction);
		return ndbDao;
	}
	else
	{
		std::cout << "DaoFactory:: not support dao: " << key <<  "for key." << std::endl;
		return NULL;
	}
}
