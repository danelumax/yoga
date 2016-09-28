/*
 * MysqlCluterManager.cpp
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#include "MysqlCluterManager.h"
#include <stdlib.h>
#include <iostream>

MysqlCluterManager* MysqlCluterManager::_instance = NULL;

MysqlCluterManager::MysqlCluterManager()
{
	_pool = InstancePool::getInstance();
}

MysqlCluterManager::~MysqlCluterManager()
{
	InstancePool::destory();
}

MysqlCluterManager* MysqlCluterManager::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new MysqlCluterManager;
	}

	return _instance;
}

void MysqlCluterManager::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void MysqlCluterManager::init()
{
	std::cout << "\nSystem start, initialize 3 ndb obj ..." << std::endl;
	for (int i=0; i<3; i++)
	{
		Ndb *ndb = new Ndb(::rand());
		std::cout << ndb->getId() << std::endl;
		_pool->addNdbIntoPool(ndb);
	}
	_pool->checkQueueStatus();
}

void MysqlCluterManager::fetchAllNdb()
{
	std::cout << "\nFetch 3 ndb from pool ..." << std::endl;
	for (int i=0; i<3; i++)
	{
		Ndb *ndb = _pool->getNdb();
		std::cout << ndb->getId() << std::endl;
	}
	_pool->checkQueueStatus();
}

void MysqlCluterManager::addExtraNdb()
{
	std::cout << "\nNdb is not enough, we will create extra 2 ndb ..." << std::endl;
	for (int i=0; i<2; i++)
	{
		Ndb *ndb = _pool->getNdb();
		std::cout << ndb->getId() << std::endl;
	}
	_pool->checkQueueStatus();
}

void MysqlCluterManager::recoverAllNdb()
{
	std::cout << "\nStart to recover ndb" << std::endl;
	std::map<Ndb*, Ndb*> NdbBusyQueue = _pool->getBusyQueue();
	std::map<Ndb*, Ndb*>::iterator iter = NdbBusyQueue.begin();
	for(; iter!=NdbBusyQueue.end(); ++iter)
	{
		std::cout << "Recover one ndb" << std::endl;
		_pool->returnNdb(iter->first);
		_pool->checkQueueStatus();
	}

	std::cout << "\nList all free queue :" << std::endl;
	std::queue<Ndb*> NdbFreeQueue = _pool->getFreeQueue();

	while(!NdbFreeQueue.empty())
	{
		Ndb* ndb = NdbFreeQueue.front();
		std::cout << ndb->getId() << std::endl;
		NdbFreeQueue.pop();
	}
}
