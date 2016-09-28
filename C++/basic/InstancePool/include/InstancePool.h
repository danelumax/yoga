/*
 * InstancePool.h
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#ifndef INSTANCEPOOL_H_
#define INSTANCEPOOL_H_

#include <map>
#include <queue>
#include <iostream>
#include <Ndb.h>

class InstancePool
{
public:
	virtual ~InstancePool();
	static InstancePool* getInstance();
	static void destory();
	Ndb* factoryNdb();
	void addNdbIntoPool(Ndb *ndb);
	Ndb* getNdb();
	void returnNdb(Ndb* ndb);
	void checkQueueStatus();
	std::queue<Ndb*> getFreeQueue();
	std::map<Ndb*, Ndb*> getBusyQueue();

private:
	InstancePool();
	static InstancePool* _instance;
	int _maxNdbPoolSize;
	std::queue<Ndb*> _freeQueue;
	/* should use vector as well, using map is for search speed. */
	std::map<Ndb*, Ndb*> _busyQueue;

    pthread_cond_t _ndbPoolCondition; // Condition for the ndb cluster connnection pool
    pthread_mutex_t _ndbPoolMutex; // Mutex for the ndb cluster connnection pool
};

#endif /* INSTANCEPOOL_H_ */
