/*
 * NdbClusterManager.h
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#ifndef NDBCLUSTERMANAGER_H_
#define NDBCLUSTERMANAGER_H_

#include <NdbApi.hpp>
#include <NdbConnectionPool.h>

class NdbClusterManager
{
public:
	virtual ~NdbClusterManager();
	static NdbClusterManager* getInstance();
	static void destory();
	int connectToCluster();
	Ndb* getNdb();
	void returnNdb(Ndb* ndb);
	void run();
	bool isNDBClusterRunning();
private:
	NdbClusterManager();
	static NdbClusterManager* _instance;

	Ndb_cluster_connection* _ndbClusterConnection;
	const char* _connectionUrl;
	NdbConnectionPool* _ndbPool;
};

#endif /* NDBCLUSTERMANAGER_H_ */
