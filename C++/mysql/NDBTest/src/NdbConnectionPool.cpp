/*
 * NdbConnectionPool.cpp
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#include "NdbConnectionPool.h"
#include <iostream>

const int NdbPoolSize = 10;

NdbConnectionPool::NdbConnectionPool()
	:_initNdbPoolSize(NdbPoolSize), _ndbClusterConnection(NULL),_databaseName("ndb_examples")
{
}

NdbConnectionPool::~NdbConnectionPool()
{
    destory();
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

Ndb* NdbConnectionPool::getNdb()
{
	if (!_freeQueue.empty())
	{
		Ndb* ndb = _freeQueue.front();
		/* must not use same ndb */
		_freeQueue.pop();
		/* let ndb obj alive */
		_busyQueue[ndb] = ndb;

		return ndb;
	}
	else
	{
		Ndb* ndb = factoryNdb();
		if (ndb)
		{
			/* let ndb obj alive */
			_busyQueue[ndb] = ndb;
			return ndb;
		}
	}

	return NULL;
}

void NdbConnectionPool::returnNdb(Ndb* ndb)
{
	std::map<Ndb*, Ndb*>::iterator iter = _busyQueue.find(ndb);
	if(iter != _busyQueue.end())
	{
		_freeQueue.push(ndb);
		_busyQueue.erase(iter);
	}
}

void NdbConnectionPool::addPoolNdb(Ndb *ndb)
{
	if (ndb)
	{
		_freeQueue.push(ndb);
	}
}

void NdbConnectionPool::destory()
{
    std::map<Ndb*, Ndb*>::iterator iter;
    for(iter = _busyQueue.begin(); iter != _busyQueue.end(); iter++)
    {
        Ndb* ndb = (*iter).first;
        if(ndb)
        {
            delete ndb;
        }
    }

    while(!_freeQueue.empty())
    {
    	Ndb* ndb = _freeQueue.front();
    	_freeQueue.pop();
    	if (ndb)
    	{
    		delete ndb;
    	}
    }

    _busyQueue.clear();
}
