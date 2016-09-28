/*
 * MysqlCluterManager.h
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#ifndef MYSQLCLUTERMANAGER_H_
#define MYSQLCLUTERMANAGER_H_

#include "InstancePool.h"

class MysqlCluterManager
{
public:
	virtual ~MysqlCluterManager();
	static MysqlCluterManager* getInstance();
	static void destory();
	void init();
	void fetchAllNdb();
	void addExtraNdb();
	void recoverAllNdb();

private:
	MysqlCluterManager();
	static MysqlCluterManager* _instance;
	InstancePool* _pool;

};

#endif /* MYSQLCLUTERMANAGER_H_ */
