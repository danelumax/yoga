/*
 * NdbConnectionPool.cpp
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#include "NdbConnectionPool.h"

NdbConnectionPool::NdbConnectionPool()
	:_initNdbPoolSize(1), _ndbClusterConnection(NULL),_databaseName("ndb_examples")
{
}

NdbConnectionPool::~NdbConnectionPool()
{
}



Ndb *NdbConnectionPool::factoryNdb()
{
	/*  represents a connection to the MySQL Cluster
	 *  the second parameter is "the database"
	 * */
	Ndb* ndb = new Ndb(_ndbClusterConnection, _databaseName.c_str());

	if (ndb && ndb->init() == 0)
	{
		return ndb;
	}
	else
	{
		if (ndb)
		{
			delete ndb;
		}
		return NULL;
	}
}

void NdbConnectionPool::factory(Ndb_cluster_connection *ndbClusterConnection)
{
	_ndbClusterConnection = ndbClusterConnection;
	for(int i=0; i<_initNdbPoolSize; i++)
	{
		Ndb* ndb = factoryNdb();
		if (ndb)
		{
			addPoolNdb(ndb);
		}
	}
}

Ndb *NdbConnectionPool::getNdb()
{
	if (!_freeQueue.empty())
	{
		Ndb* ndb = _freeQueue.front();
		//_freeQueue.pop();

		return ndb;
	}

	return NULL;
}

void NdbConnectionPool::addPoolNdb(Ndb *ndb)
{
	if (ndb)
	{
		_freeQueue.push(ndb);
	}
}
