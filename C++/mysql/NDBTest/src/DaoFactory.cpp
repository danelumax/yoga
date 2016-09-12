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

	return transaction;
}

NdbDao *DaoFactory::factoryDao()
{
	NdbDao* dao = new NdbDao();
	return dao;
}
