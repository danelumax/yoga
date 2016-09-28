//============================================================================
// Name        : InstancePool.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <map>
#include <queue>
#include <Ndb.h>
#include <InstancePool.h>
#include <MysqlCluterManager.h>

int main()
{
	MysqlCluterManager* manager = MysqlCluterManager::getInstance();

	manager->init();

	manager->fetchAllNdb();

	manager->addExtraNdb();

	manager->recoverAllNdb();

	MysqlCluterManager::destory();

	return 0;
}
