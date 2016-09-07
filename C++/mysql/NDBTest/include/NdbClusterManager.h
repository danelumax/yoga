/*
 * NdbClusterManager.h
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#ifndef NDBCLUSTERMANAGER_H_
#define NDBCLUSTERMANAGER_H_

#include <NdbApi.hpp>

class NdbClusterManager
{
public:
	virtual ~NdbClusterManager();
	static NdbClusterManager* getInstance();
	static void destory();
	int connectToCluster();
	Ndb* getNdb();
private:
	NdbClusterManager();
	static NdbClusterManager* _instance;

	Ndb_cluster_connection* _ndbClusterConnection;
	Ndb* _ndb;
	const char* _connectionUrl;
};

#endif /* NDBCLUSTERMANAGER_H_ */
