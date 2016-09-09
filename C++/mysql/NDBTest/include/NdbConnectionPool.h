/*
 * NdbConnectionPool.h
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#ifndef NDBCONNECTIONPOOL_H_
#define NDBCONNECTIONPOOL_H_

#include <queue>
#include <string>
#include <NdbApi.hpp>

class NdbConnectionPool
{
public:
	NdbConnectionPool();
	virtual ~NdbConnectionPool();
	void factory(Ndb_cluster_connection* ndbClusterConnection);
	Ndb* getNdb();
private:
	Ndb* factoryNdb();
	void addPoolNdb(Ndb* ndb);

	std::queue<Ndb*> _freeQueue;
	int _initNdbPoolSize;
	Ndb_cluster_connection* _ndbClusterConnection;
	std::string _databaseName;
};

#endif /* NDBCONNECTIONPOOL_H_ */
