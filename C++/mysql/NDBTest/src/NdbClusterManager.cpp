/*
 * NdbClusterManager.cpp
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#include "NdbClusterManager.h"
#include "NdbOperationTransaction.h"
#include <iostream>

NdbClusterManager* NdbClusterManager::_instance = NULL;

NdbClusterManager::NdbClusterManager()
	:_connectionUrl("127.0.0.1")
{
	_ndbPool = new NdbConnectionPool();
	/* ndb_init must be called first */
	ndb_init();
}

NdbClusterManager::~NdbClusterManager()
{
	/* deleting ndb before Ndb_cluster_connection */
	delete _ndbPool;
	delete _ndbClusterConnection;
	_ndbClusterConnection = NULL;
	_ndbPool = NULL;
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

	ndb_end(0);
}

int NdbClusterManager::connectToCluster()
{
	int ret = 0;
	/* a object, which represents one connection to a cluster management server which IP is _connectionUrl.
	 * creating a Ndb_cluster_connection first before creating NDB
	 * */
	_ndbClusterConnection = new Ndb_cluster_connection(_connectionUrl);

	/* connection operation */
	if (_ndbClusterConnection->connect(0, 0, 0) == 0)
	{
		/* wait for the connection to reach one or more data nodes */
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
	return _ndbPool->getNdb();
}

void NdbClusterManager::returnNdb(Ndb* ndb)
{
	if (_ndbPool)
	{
		_ndbPool->returnNdb(ndb);
	}
}

void NdbClusterManager::run()
{
	connectToCluster();
	_ndbPool->factory(_ndbClusterConnection);
}

bool NdbClusterManager::isNDBClusterRunning()
{
	return true;
}
