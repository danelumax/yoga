/*
 * NdbClusterManager.cpp
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#include "NdbClusterManager.h"
#include <iostream>

NdbClusterManager* NdbClusterManager::_instance = NULL;

NdbClusterManager::NdbClusterManager()
	:_connectionUrl("127.0.0.1")
{
	/* ndb_init must be called first */
	ndb_init();
}

NdbClusterManager::~NdbClusterManager()
{
	delete _ndb;
	delete _ndbClusterConnection;
	ndb_end(0);
}

NdbClusterManager* NdbClusterManager::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new NdbClusterManager();
	}

	return _instance;
}

void NdbClusterManager::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}

int NdbClusterManager::connectToCluster()
{
	int ret = 0;
	_ndbClusterConnection = new Ndb_cluster_connection(_connectionUrl);

	if (_ndbClusterConnection->connect(0, 0, 0) == 0)
	{
		if (_ndbClusterConnection->wait_until_ready(10, 0) < 0)
		{
			std::cout << "connect fail." << std::endl;
			ret = 1;
		}
	}

	return ret;
}

Ndb* NdbClusterManager::getNdb()
{
	_ndb = new Ndb(_ndbClusterConnection, "ndb_examples" );
	if (_ndb->init() != 0)
	{
		std::cout << "NdbConnectionPool::factoryNdb failed to initialize NDB object." << std::endl;
		return NULL;
	}

	return _ndb;
}
